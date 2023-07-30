from typing import List
from fastapi import APIRouter, HTTPException, Request

from slowapi import Limiter
from slowapi.util import get_remote_address
from payloads import RedditPostPayload, RedditPostsListPayload
from managers.submissions import SubmissionsManager
from viewsets.helpers import check_key
from fastapi_utils.tasks import repeat_every

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()
submission_manager = SubmissionsManager()

@router.post("/", status_code=201)
@limiter.limit("100/minute")
def create_reddit_scheduled_submission(submission: RedditPostPayload, request: Request):
    check_key(request)
    return submission_manager.create_submission(submission)

@router.get("/{rowid}/", response_model=RedditPostPayload)
def read_reddit_scheduled_submission(request: Request, rowid: int):  # Update parameter name here
    check_key(request)
    submission = submission_manager.read_submission(rowid)  # Update function call here
    if not submission:
        raise HTTPException(status_code=404, detail="Not Found")
    return submission

@router.put("/{rowid}/", status_code=200)
def update_reddit_scheduled_submission(
    rowid: int, submission: RedditPostPayload, request: Request
):
    check_key(request)
    submission.rowid = rowid
    existing_submission = submission_manager.read_submission(rowid)
    if not existing_submission:
        raise HTTPException(status_code=404, detail="Not Found")
    submission_manager.update_submission(existing_submission)
    return {"result": "Success"}

@router.delete("/{rowid}/", status_code=200)
def delete_reddit_scheduled_submission(request: Request, rowid: int):  # Update parameter name here
    check_key(request)
    existing_submission = submission_manager.read_submission(rowid)  # Update function call here
    if not existing_submission:
        raise HTTPException(status_code=404, detail="Not Found")
    submission_manager.delete_submission(rowid)  # Update function call here
    return {"result": "Success"}

@router.get("/", response_model=RedditPostsListPayload)
def list_reddit_scheduled_submissions(request: Request, page: int = 1, per_page: int = 10):
    check_key(request)
    submissions = submission_manager.list_submissions(page, per_page)

    result = RedditPostsListPayload(
        page=page, per_page=per_page, count=len(submissions), users=submissions
    )
    return result

@router.on_event("startup")
@repeat_every(seconds=30)
def check_scheduled_submissions():
    submission_manager.check_scheduled_submissions()
