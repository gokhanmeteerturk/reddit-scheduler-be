from ast import List
import glob
import os
import shutil
from typing import Optional
from fastapi import Depends, FastAPI, File, HTTPException, Query, Request, UploadFile
import requests
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from settings import ALLOWED_IMG_EXTENSIONS, IMG_DIR

from viewsets.users import router as users_router
from viewsets.scheduled_submissions import router as scheduled_submissions_router
from viewsets.helpers import check_key, is_valid_image, generate_unique_filename, is_valid_video, save_image, save_video, validate_img_extension, validate_img_size




limiter = Limiter(key_func=get_remote_address)
app = FastAPI(middleware=[
    Middleware(CORSMiddleware, allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)
])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

app.mount("/images", StaticFiles(directory="images"), name="images")


@app.post("/download_image/")
async def download_image(image_url: str):
    from PIL import Image
    # Check if the provided URL matches the expected format
    if not image_url.startswith("https://i.redd.it/") or (not image_url.endswith(".jpg") and not image_url.endswith(".png")):
        return {"error": "Invalid image URL. It should be in the format: https://i.redd.it/{slug}.jpg"}

    try:
        # Download the image from the provided URL
        response = requests.get(image_url)
        response.raise_for_status()

        filename = generate_unique_filename(image_url.split("/")[-1])

        with open(os.path.join(IMG_DIR, filename), "wb") as f:
            f.write(response.content)

        # Generate and save the thumbnail
        thumbnail_filename = f"thumb_{filename}"
        image = Image.open(os.path.join(IMG_DIR, filename))
        thumbnail = image.copy()
        thumbnail.thumbnail((96, 96))
        thumbnail.save(os.path.join(IMG_DIR, thumbnail_filename))

        return {"filename": filename}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to download image: {e}"}


@app.post("/upload_image/")
async def upload_image(request: Request, file: UploadFile):
    check_key(request)
    validate_img_extension(file.filename)
    validate_img_size(file.file)
    image = is_valid_image(file)
    if image is None:
        return JSONResponse(content={"error": "Invalid image file."}, status_code=400)

    new_filename = generate_unique_filename(file.filename)
    thumbnail_filename = f"thumb_{new_filename}"
    thumbnail = image.copy()
    thumbnail.thumbnail((96,96))
    save_image(image, new_filename)
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



def list_images(
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=1),
):
    images = [f for f in glob.glob(os.path.join(IMG_DIR, "*")) if not os.path.basename(f).startswith("thumb_") and os.path.splitext(f)[-1][1:].lower() in ALLOWED_IMG_EXTENSIONS]

    images.sort(key=os.path.getmtime, reverse=True)
    images = [i.replace("\\", "/").replace(IMG_DIR, "") for i in images]

    # Pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_images = images[start_idx:end_idx]

    return {"results": paginated_images}

@app.get("/list_images/")
def get_images(
    request: Request,
    page: Optional[int] = Query(1, ge=1),
    per_page: Optional[int] = Query(100, ge=1),
):
    check_key(request)
    return list_images(page=page, per_page=per_page)

@app.get("/init/")
@limiter.limit("5/minute")
def initialize(request: Request):
    from install import initialize_once

    master_key = initialize_once()
    if master_key is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return {"master_key": master_key}
