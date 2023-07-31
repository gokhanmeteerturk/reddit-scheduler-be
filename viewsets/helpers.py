from fastapi import HTTPException
from cursor import Database


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text  # or whatever


def check_key(request):
    key = request.headers.get("authorization")
    if key is None or not Database().is_master_key_correct(
        remove_prefix(key, "Basic ")
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")
