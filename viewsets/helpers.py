import os
import shutil
from fastapi import HTTPException
from cursor import Database
from PIL import Image
from hashids import Hashids
import time

from settings import IMG_DIR, VIDEO_DIR


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

def is_valid_image(file):
    try:
        image = Image.open(file.file)
        image.verify()
        return image
    except:
        return None

def save_image(image, filename):
    image.save(os.path.join(IMG_DIR, filename))

def create_thumbnail(image, size=(96, 96)):
    return image.copy().thumbnail(size)

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
