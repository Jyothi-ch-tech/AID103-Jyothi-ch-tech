import datetime
try:
    from ..utils.storage_utils import load, save
except ImportError:
    from utils.storage_utils import load, save

def add_farm(email, crop_type, sow_date, location):
    farms = load("farms")
    doc = {
        "email": email,
        "crop_type": crop_type,
        "sow_date": sow_date,
        "location": location,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    farms.append(doc)
    save("farms", farms)
    return {"status": "ok"}

def get_farms(email):
    farms = load("farms")
    return [f for f in farms if f.get("email")==email]
