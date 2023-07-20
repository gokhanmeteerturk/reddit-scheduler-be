from typing import Union

from fastapi import FastAPI, HTTPException, Request
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

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

def check_key(request):
    key = request.headers.get('authorization')
    if key is None or not Database().is_master_key_correct(remove_prefix(key,'Basic ')):
        raise HTTPException(status_code=401, detail="Unauthorized")

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever