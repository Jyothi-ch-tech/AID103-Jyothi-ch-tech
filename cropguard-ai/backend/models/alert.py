import datetime
try:
    from ..utils.storage_utils import load, save
except ImportError:
    from utils.storage_utils import load, save

def create_alert(email, disease, confidence, severity, location):
    alerts = load("alerts")
    doc = {
        "email": email,
        "disease": disease,
        "confidence": confidence,
        "severity": severity,
        "location": location,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    alerts.append(doc)
    save("alerts", alerts)
    return {"status": "ok"}

def get_alerts(email=None):
    alerts = load("alerts")
    items = [a for a in alerts if (email is None or a.get("email")==email)]
    items.sort(key=lambda x: x.get("created_at",""), reverse=True)
    return items
