from fastapi import APIRouter, HTTPException, Request
from typing import Type, Union

from slowapi import Limiter
from slowapi.util import get_remote_address
from payloads import RedditUserPayload, RedditUserPayloadWithCrosspostables, RedditUsersListPayload
from managers.users import UserManager
from viewsets.helpers import check_key

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()
user_manager = UserManager()


@router.post("/", status_code=201)
@limiter.limit("20/minute")
def create_reddit_user(user: RedditUserPayload, request: Request):
    check_key(request)
    return user_manager.create_user(user)


@router.get("/", response_model=RedditUsersListPayload)
def list_reddit_users(request: Request, page: int = 1, per_page: int = 10):
    check_key(request)
    users = user_manager.list_users(page, per_page)
    result = RedditUsersListPayload(
        page=page, per_page=per_page, count=len(users), users=users
    )
    return result


@router.get("/{username}/", response_model=RedditUserPayloadWithCrosspostables)
def read_reddit_user(username: str, request: Request, with_crosspostable_subs:bool = False):
    check_key(request)
    user = user_manager.read_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="Not Found")
    crosspostable_subs = []
    if with_crosspostable_subs:
        crosspostable_subs = user_manager.read_crosspostable_subs(username)
    user = RedditUserPayloadWithCrosspostables.from_user_payload(user, crosspostable_subs)
    print(user)
    return user


@router.put("/{username}/", status_code=200)
def update_reddit_user(username: str, user: RedditUserPayload, request: Request):
    check_key(request)
    existing_user = user_manager.read_user(username)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Not Found")
    user_manager.update_user(user)
    return {"result": "Success"}


@router.delete("/{username}/", status_code=200)
def delete_reddit_user(request: Request, username: str):
    check_key(request)
    existing_user = user_manager.read_user(username)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Not Found")
    user_manager.delete_user(username)
    return {"result": "Success"}
