try:
    from ..utils.storage_utils import load
except ImportError:
    from utils.storage_utils import load

def get_reports():
    alerts = load("alerts")
    agg = {}
    for a in alerts:
        d = a.get("disease")
        if d not in agg:
            agg[d] = {"count": 0, "sum_conf": 0.0}
        agg[d]["count"] += 1
        agg[d]["sum_conf"] += float(a.get("confidence", 0))
    return [{"disease": k, "count": v["count"], "avg_confidence": (v["sum_conf"] / v["count"] if v["count"] else 0)} for k, v in agg.items()]
