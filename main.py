import os
import shutil
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from settings import ALLOWED_IMG_EXTENSIONS, IMG_MAX_FILE_SIZE

from viewsets.users import router as users_router
from viewsets.scheduled_submissions import router as scheduled_submissions_router
from viewsets.helpers import check_key, create_thumbnail, is_valid_image, generate_unique_filename, is_valid_video, save_image, save_video

from starlette_validation_uploadfile import ValidateUploadFileMiddleware



limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(
    users_router,
    prefix="/reddit_users",
    tags=["reddit_users"],
    dependencies=[Depends(get_remote_address)],
)
app.include_router(
    scheduled_submissions_router,
    prefix="/scheduled_submissions",
    tags=["scheduled_submissions"],
    dependencies=[Depends(get_remote_address)],
)


app.add_middleware(
    ValidateUploadFileMiddleware,
    app_path=[
        "/upload_image/"
    ],
    max_size=IMG_MAX_FILE_SIZE,
    file_type=ALLOWED_IMG_EXTENSIONS
)

@app.post("/upload_image/")
async def upload_image(request: Request, file: UploadFile = File(...)):
    check_key(request)

    image = is_valid_image(file)
    if image is None:
        return JSONResponse(content={"error": "Invalid image file."}, status_code=400)

    new_filename = generate_unique_filename(file.filename)
    save_image(image, new_filename)

    thumbnail_filename = f"thumb_{new_filename}"
    thumbnail = create_thumbnail(image)
    save_image(thumbnail, thumbnail_filename)

    return {"filename": new_filename}


"""
@app.add_route("/upload_video/", methods=["POST"])
async def upload_video(request: Request, file: UploadFile = File(...)):
    check_key(request)

    # IMPORTANT: below function ain't doing anything right now!
    video = is_valid_video(file)
    if video is None:
        return JSONResponse(content={"error": "Invalid video file."}, status_code=400)

    new_filename = generate_unique_filename(file.filename)
    save_video(video, new_filename)

    return {"filename": new_filename}
"""

@app.get("/init/")
@limiter.limit("5/minute")
def initialize(request: Request):
    from install import initialize_once

    master_key = initialize_once()
    if master_key is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return {"master_key": master_key}
