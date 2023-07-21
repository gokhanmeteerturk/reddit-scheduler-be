from typing import Union

from fastapi import FastAPI, HTTPException, Request
from fastapi_utils.tasks import repeat_every

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from cursor import Database
from payloads import RedditUserPayload


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/init/")
@limiter.limit("5/minute")
def initialize(request: Request):
    from install import initialize_once

    master_key = initialize_once()
    if master_key is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return {'master_key':master_key}

@app.post("/test/")
@limiter.limit("1000/minute")
def test(request: Request):
    check_key(request)
    return {"result":"Success"}

# @app.post("/post/")
# @limiter.limit("1000/minute")
# def shedule_post(request: Request):
#     check_key(request)
#     return {"result":"Success"}

@app.post("/reddit_user/")
@limiter.limit("20/minute")
def create_reddit_user(request: Request, user:RedditUserPayload):
    check_key(request)
    db = Database()
    c = db.connect()
    c.execute("INSERT INTO users VALUES(?, ?, ?, ?)",(user.username, user.password, user.client_id, user.client_secret))
    db.connection.commit()
    db.disconnect()
    return {"result":"Success"}

@app.get("/reddit_user/{username}/")
def read_reddit_user(request: Request, username: str):
    check_key(request)
    user = None
    db = Database()
    c = db.connect()
    c.execute("SELECT * FROM users WHERE username = ? ORDER BY rowid ASC LIMIT 1", (username,))
    user_tuple = c.fetchone()
    db.disconnect()
    if user_tuple:
        user = RedditUserPayload.from_tuple(user_tuple)
    else:
        raise HTTPException(status_code=404, detail="Not Found")
    return user

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

def check_key(request):
    key = request.headers.get('authorization')
    if key is None or not Database().is_master_key_correct(remove_prefix(key,'Basic ')):
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.on_event("startup")
@repeat_every(seconds=30)
def check_scheduled_submissions():
    try:
        # Find and handle scheduled submissions
        pass
    except Exception as e:
        print(e)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever