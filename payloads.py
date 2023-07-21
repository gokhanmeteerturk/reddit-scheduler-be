from pydantic import BaseModel

class CustomBaseModel(BaseModel):
    @classmethod
    def from_tuple(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), tpl)})

    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), tpl)})


class RedditUserPayload(CustomBaseModel):
    username: str
    password: str
    client_id: str
    client_secret: str

class RedditPostPayload(CustomBaseModel):
    username: str
    sub: str
    title: str
    text: str | None = None
    link: str | None = None
    image_name: str | None = None
    video: str | None = None
    flairid: str | None = None
    nsfw: bool | None = None