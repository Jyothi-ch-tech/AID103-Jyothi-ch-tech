import datetime
import bcrypt
try:
    from ..utils.storage_utils import load, save
except ImportError:
    from utils.storage_utils import load, save

def create_user(email, password, name):
    users = load("users")
    if any(u.get("email")==email for u in users):
        return None
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    doc = {"email": email, "password": hashed, "name": name, "created_at": datetime.datetime.utcnow().isoformat()}
    users.append(doc)
    save("users", users)
    return {"email": email, "name": name}

def verify_user(email, password):
    users = load("users")
    u = next((u for u in users if u.get("email")==email), None)
    if not u:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), u["password"].encode("utf-8"))
