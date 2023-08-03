from typing import List
from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    @classmethod
    def from_tuple(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), tpl)})

    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), tpl)})


class CrosspostRequestPayload(BaseModel):
    sub: str
    planned_unix_datetime: int | None = None


class RedditUserPayload(CustomBaseModel):
    username: str
    password: str
    client_id: str
    client_secret: str


class RedditUserPayloadWithCrosspostables(RedditUserPayload):
    crosspostable_subs: List = []

    @classmethod
    def from_user_payload(
        cls,
        user: RedditUserPayload,
        crosspostable_subs: List = [],
    ):
        return cls(
            **dict(user), crosspostable_subs=crosspostable_subs
        )


class RedditUsersListPayload(BaseModel):
    page: int
    per_page: int
    count: int
    users: List[RedditUserPayload]


class RedditPostPayload(CustomBaseModel):
    rowid: int | None = None
    planned_unix_datetime: int | None = None
    status: str | None = None
    username: str
    sub: str
    title: str
    text: str | None = None
    link: str | None = None
    image_name: str | None = None
    video: str | None = None
    flairid: str | None = None
    nsfw: bool | None = False
    submission_id: str | None = None
    crosspost_of: int | None = None
    crosspost_requests: List[CrosspostRequestPayload] = []


class RedditPostsListPayload(BaseModel):
    page: int
    per_page: int
    count: int
    users: List[RedditPostPayload]
