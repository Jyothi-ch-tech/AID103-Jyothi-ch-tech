import os
import json
try:
    from ..config import get_config
except ImportError:
    from config import get_config

def _base():
    path = get_config()["STORAGE_PATH"]
    os.makedirs(path, exist_ok=True)
    return path

def _file(name):
    return os.path.join(_base(), name + ".json")

def load(name):
    fp = _file(name)
    if not os.path.exists(fp):
        return []
    with open(fp, "r", encoding="utf-8") as f:
        return json.load(f)

def save(name, data):
    fp = _file(name)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
