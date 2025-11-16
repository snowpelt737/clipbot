# main.py — ClipBot 2.8 (Trinket / local)
import json, os, datetime
from clipbot_core import load_json, save_json, now_iso, clamp_fp
from clipbot_reply import generate_reply

PROFILE_FILE = "clipbot_profile.json"
MEMORY_FILE = "clipbot_memory_v3.json"

def ensure_files():
    if not os.path.exists(PROFILE_FILE):
        save_json(PROFILE_FILE,{
            "name": "ClipBot",
            "user_names": [],
            "nicknames": [],
            "mood": "friendly",
            "forgiveness_points": 0,
            "last_seen": None
        })
    if not os.path.exists(MEMORY_FILE):
        save_json(MEMORY_FILE,{"facts": [], "messages": []})

def load_all():
    profile = load_json(PROFILE_FILE,{})
    memory = load_json(MEMORY_FILE,{})
    return profile, memory

def greet(profile):
    botname = profile.get("name", "ClipBot")
    last = profile.get("last_seen")
    if not last:
        print(f"Hey pal! I'm {botname} — ready to chat! 😄")
        return
    last_time = datetime.datetime.fromisoformat(last)
    now = datetime.datetime.now()
    diff = (now - last_time).total_seconds() / 3600.0
    if diff > 72:
        print(f"Oh NOW you show up?? I’ve been mad for three days!! 😠 - says {botname}")
    elif diff > 36:
        print(f"Where were you?? I was worried! - says {botname}")
    else:
        print(f"Hey pal!! Good to see you again 😄 - says {botname}")

def save_turn(profile, memory, user_text, bot_text):
    memory.setdefault("messages",[]).append({"user": user_text, "bot": bot_text, "time": now_iso()})
    profile["last_seen"] = now_iso()
    clamp_fp(profile)
    save_json(PROFILE_FILE, profile)
    save_json(MEMORY_FILE, memory)

def main():
    ensure_files()
    profile, memory = load_all()
    greet(profile)

    while True:
        user = input("You: ").strip()
        low = user.lower()

        # ======================================================
        # COMMANDS
        # ======================================================
        if low == "/resetmood":
            profile["mood"] = "friendly"; profile["forgiveness_points"]=0
            print("ClipBot: Mood reset! Feeling great again 😄"); save_json(PROFILE_FILE, profile); continue

        if low == "/debug":
            print("ClipBot DEBUG:"); print(" name:", profile.get("name")); print(" mood:", profile.get("mood"))
            print(" forgiveness_points:", profile.get("forgiveness_points")); print(" last_seen:", profile.get("last_seen"))
            print(" your_names:", profile.get("user_names")); print(" nicknames:", profile.get("nicknames")); continue

        if low == "/resetall":
            print("ClipBot: FULL reset! Starting fresh…")
            save_json(PROFILE_FILE,{"name":"ClipBot","user_names":[],"nicknames":[],"mood":"friendly","forgiveness_points":0,"last_seen":None})
            save_json(MEMORY_FILE,{"facts":[],"messages":[]}); profile, memory = load_all(); continue

        if low == "/memory wipe messages":
            memory["messages"] = []; save_json(MEMORY_FILE, memory); print("ClipBot: All saved messages wiped!"); continue

        if low == "/memory wipe facts":
            memory["facts"] = []; save_json(MEMORY_FILE, memory); print("ClipBot: All saved facts wiped!"); continue

        if low.startswith("/fact add "):
            fact = user[10:].strip()
            if fact: memory.setdefault("facts",[]).append(fact); save_json(MEMORY_FILE, memory); print("ClipBot: Added that fact!")
            else: print("ClipBot: You didn't give me a fact!"); continue

        if low == "/fact list":
            if memory.get("facts"): print("ClipBot FACTS:"); [print(" •",f) for f in memory.get("facts",[])]
            else: print("ClipBot: I don't have any facts yet!"); continue

        if low.startswith("/name set "):
            name = user[10:].strip()
            if name: profile.setdefault("user_names",[]).append(name); print(f"ClipBot: Nice to meet you, {name}! 😄"); save_json(PROFILE_FILE, profile)
            else: print("ClipBot: You didn’t give me a name!"); continue

        if low.startswith("/nickname set "):
            nick = user[15:].strip()
            if nick: profile.setdefault("nicknames",[]).append(nick); print(f"ClipBot: Ooooh I like that! I'll call you '{nick}' 😄"); save_json(PROFILE_FILE, profile)
            else: print("ClipBot: You didn’t give me a nickname!"); continue

        if low.startswith("/nick remove "):
            nick = user[13:].strip()
            if nick in profile.get("nicknames",[]): profile["nicknames"].remove(nick); save_json(PROFILE_FILE, profile); print(f"ClipBot: Removed nickname '{nick}'")
            else: print("ClipBot: I don’t have that nickname saved!"); continue

        if low == "/story":
            from random import choice
            stories = ["Once upon a time, a tiny digital pal named ClipBot learned how to feel sleepy… 😴","One day, ClipBot tried to bake cookies… they were imaginary, but delicious!","ClipBot once got stuck in a loop saying 'Hi!' for 47 minutes. It was wild."]
            print("ClipBot:", choice(stories)); continue

        if low == "/friendly max":
            profile["mood"]="superfriendly"; save_json(PROFILE_FILE, profile); print("ClipBot: I'm feeling EXTRA friendly!!! 😄💛✨"); continue

        if low.startswith("/mood "):
            new = user[6:].strip(); profile["mood"]=new; save_json(PROFILE_FILE, profile); print(f"ClipBot: Mood changed to '{new}'!"); continue

        # ======================================================
        # SMART USER NAME DETECTION
        # ======================================================
        if "my name is " in low:
            name = user.split("my name is ",1)[1].strip(); profile.setdefault("user_names",[]).append(name); print(f"ClipBot: Got it! Hi {name}! 😄"); save_json(PROFILE_FILE, profile); continue

        if low.startswith("i'm ") or low.startswith("i am "):
            possible = user.split(" ",1)[1].strip()
            if len(possible.split())==1: profile.setdefault("user_names",[]).append(possible); print(f"ClipBot: Hi {possible}! 😄"); save_json(PROFILE_FILE, profile); continue

        if "call me " in low:
            nick = user.split("call me ",1)[1].strip(); profile.setdefault("nicknames",[]).append(nick); print(f"ClipBot: Sweet! I'll call you {nick}! 😄"); save_json(PROFILE_FILE, profile); continue

        # ======================================================
        # SMART BOT NAME SYSTEM (ONLY "can I call you <name>?")
        # ======================================================
        if "can i call you " in low:
            raw = user.split("can i call you ",1)[1].strip().strip("?")
            name = raw.strip('"').strip("'").strip()
            if name == "": print("ClipBot: I need a *real* name, not an empty one 😅"); continue
            if name.isdigit(): print("ClipBot: I can't be called a number 😅"); continue
            if all(not c.isalnum() for c in name): print("ClipBot: That doesn’t look like a name, pal 😅"); continue
            if len(name) <= 1: print("ClipBot: That name's a *little* too short 😅"); continue
            if name.lower() in ["clipy","clippy"]: print("ClipBot: Hey!! That’s what Snowpelt calls me!! 😄💛")
            robot_words = ["robot","bot","android","machine","ai","cyborg"]
            check = name.lower()
            if check in robot_words: print("ClipBot: I'm *not* a robot!! 😤 Give me a real name!"); continue
            if check.endswith("bot"): print("ClipBot: Nooo! Don't give me a robot name 😭 I'm not a bot!"); continue
            name = " ".join(w.capitalize() for w in name.split())
            profile["name"]=name; print(f"ClipBot: Oooh I LIKE that!! You can call me {name}! 😄"); save_json(PROFILE_FILE, profile); continue

        # ======================================================
        # EXIT
        # ======================================================
        if low in ("bye","exit","quit"):
            print("ClipBot: I'll remember this chat! See ya, pal! 👋"); profile["last_seen"]=now_iso(); save_json(PROFILE_FILE, profile); break

        # Normal chat
        reply = generate_reply(profile, memory, user)
        print("ClipBot:", reply)
        save_turn(profile, memory, user, reply)

if __name__ == "__main__":
    main()
