import os
import uuid
try:
    from ..config import get_config
except ImportError:
    from config import get_config

def ensure_storage():
    path = get_config()["STORAGE_PATH"]
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

def save_upload(file_storage):
    base = ensure_storage()
    ext = os.path.splitext(file_storage.filename)[1].lower()
    name = str(uuid.uuid4()) + (ext if ext else ".jpg")
    dest = os.path.join(base, name)
    file_storage.save(dest)
    return dest, name
