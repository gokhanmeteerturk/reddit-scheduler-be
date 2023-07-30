from fastapi import Depends, FastAPI, HTTPException, Request

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from viewsets.users import router as users_router
from viewsets.scheduled_submissions import router as scheduled_submissions_router

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(users_router, prefix="/reddit_users", tags=["reddit_users"], dependencies=[Depends(get_remote_address)])
app.include_router(scheduled_submissions_router, prefix="/scheduled_submissions", tags=["scheduled_submissions"], dependencies=[Depends(get_remote_address)])


@app.get("/init/")
@limiter.limit("5/minute")
def initialize(request: Request):
    from install import initialize_once

    master_key = initialize_once()
    if master_key is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return {"master_key": master_key}
