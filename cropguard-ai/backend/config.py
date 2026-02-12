import os

def get_config():
    return {
        "MONGODB_URI": os.environ.get("MONGODB_URI", "mongodb://localhost:27017/cropguard"),
        "MODEL_PATH": os.environ.get("MODEL_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "model", "model.h5")),
        "STORAGE_PATH": os.environ.get("STORAGE_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage")),
        "PORT": os.environ.get("PORT", "5000")
    }
