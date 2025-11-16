# clipbot_core.py — Core utilities for ClipBot 2.8
import json, datetime, os

def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def now_iso():
    return datetime.datetime.now().isoformat()

def clamp_fp(profile):
    fp = profile.get("forgiveness_points", 0)
    if fp > 10: fp = 10
    if fp < -10: fp = -10
    profile["forgiveness_points"] = fp
    return fp
