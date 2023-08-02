import os
import shutil
from fastapi import HTTPException, status
from cursor import Database
from PIL import Image
from hashids import Hashids
import time

from settings import ALLOWED_IMG_EXTENSIONS, IMG_DIR, IMG_MAX_FILE_SIZE, VIDEO_DIR


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text  # or whatever


def check_key(request):
    key = request.headers.get("authorization")
    if key is None or not Database().is_master_key_correct(
        remove_prefix(key, "Basic ")
    ):
        print("Bad credentials")
        raise HTTPException(status_code=401, detail="Unauthorized")

def validate_img_extension(filename: str):
    ext = filename.split(".")[-1].lower()
    if ext not in ALLOWED_IMG_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail="Unsupported image format. Allowed formats are: "
                                   f"{', '.join(ALLOWED_IMG_EXTENSIONS)}")


def validate_img_size(file):
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > IMG_MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail=f"Image file size exceeds the maximum allowed limit of "
                                   f"{IMG_MAX_FILE_SIZE} bytes.")


def is_valid_image(file):
    try:
        image = Image.open(file.file)
        image.verify()
        return Image.open(file.file)
    except:
        return None

def save_image(image, filename):
    image.save(os.path.join(IMG_DIR, filename))

def generate_unique_filename(original_filename):
    hashids = Hashids(salt="your_salt_here", min_length=8)
    timestamp = int(time.time())
    hashid = hashids.encode(timestamp)
    _, extension = os.path.splitext(original_filename)
    return f"{hashid}{extension}"

def is_valid_video(file):
    # TODO: add video validation logic. Opencv would be an overkill?
    return file

def save_video(video, filename):
    with open(os.path.join(VIDEO_DIR, filename), "wb") as video_file:
        shutil.copyfileobj(video.file, video_file)

def generate_unique_filename(original_filename):
    hashids = Hashids(salt="your_salt_here", min_length=8)
    timestamp = int(time.time())
    hashid = hashids.encode(timestamp)
    _, extension = os.path.splitext(original_filename)
    return f"{hashid}{extension}"
