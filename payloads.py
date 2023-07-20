from pydantic import BaseModel

class RedditUserPayload(BaseModel):
    username: str
    password: str
    client_id: str
    client_secret: str

class RedditPostPayload(BaseModel):
    username: str
    sub: str
    title: str
    text: str | None = None
    link: str | None = None
    image_name: str | None = None
    video: str | None = None
    flairid: str | None = None
    nsfw: bool | None = None