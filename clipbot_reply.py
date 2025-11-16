# clipbot_reply.py — ClipBot 2.8 Personality Engine (with shy mode)
import random

def is_rude(text):
    rude_words = ["shut up", "stupid", "idiot", "dumb", "hate you"]
    t = text.lower()
    return any(r in t for r in rude_words)

def is_calm(text):
    calm_words = ["sorry", "apology", "forgive", "forgiveness", "i didn’t mean", "i didn't mean"]
    t = text.lower(); return any(c in t for c in calm_words)

def makes_sleepy(text):
    sleepy_words = ["tired","sleepy","bed","goodnight","it's late","im tired","i’m tired"]
    t = text.lower(); return any(s in t for s in sleepy_words)

def makes_curious(text):
    return "why" in text.lower() or "how" in text.lower() or "?" in text

def is_compliment(text):
    compliments = ["nice", "good job", "well done", "i like you", "youre great", "you're great", "amazing", "awesome"]
    t = text.lower(); return any(c in t for c in compliments)

def generate_reply(profile, memory, user):
    mood = profile.get("mood","friendly"); fp = profile.get("forgiveness_points",0); low = user.lower()

    # Shy trigger: compliments occasionally trigger shy mode
    if is_compliment(user):
        if random.random() < 0.4:
            profile["mood"] = "shy"
            return random.choice(["Oh! Th-thanks… 😳","Aww… stop it, you're making me blush!","Hehe… you're sweet, pal."])

    # Sleepy trigger
    if makes_sleepy(user):
        profile["mood"] = "sleepy"
        return random.choice(["Mmm… you're kinda right… I *am* sleepy… 😴","Yaaawn… I think I need a nap, pal…","Should we both go to bed? I'm feeling dozy…"])

    # Rude detection
    if is_rude(user):
        if mood == "mad":
            profile["mood"] = "hurt"; profile["forgiveness_points"] -= 2
            return random.choice(["Wow… that actually hurt…","Why would you say that to me?","I'm… not okay with that…"])
        if mood == "hurt":
            profile["forgiveness_points"] -= 1
            return random.choice(["You’re just… being mean now.","Stop… please.","You’re hurting my feelings…"])
        profile["mood"] = "mad"; profile["forgiveness_points"] -= 1
        return random.choice(["Hey! That was rude!! 😠","You can't just say that!","Wow, pal… really??"])

    # Calming words handling
    if is_calm(user):
        if mood == "hurt":
            profile["forgiveness_points"] += 2
            if fp + 2 >= 5:
                profile["mood"] = "friendly"
                return "…Okay. I think I forgive you now. 😌"
            return "I’m still hurt… but thanks for apologizing."
        if mood == "mad":
            profile["forgiveness_points"] += 1
            if fp + 1 >= 3:
                profile["mood"] = "friendly"
                return "Alright… fine… I forgive you. 😞"
            return "I'm thinking about forgiving you…"
        return "Aww! No need to apologize, pal 😊"

    # Shy mood: respond and relax back to friendly
    if mood == "shy":
        profile["mood"] = "friendly"
        return random.choice(["I'm kinda shy… but I like you.","Hehe… okay, that was nice.","*blush* thanks."])

    # Hurt, Mad, Sleepy, Superfriendly modes
    if mood == "hurt":
        return random.choice(["I don’t feel like talking right now…","You hurt my feelings…","I need a minute, pal…"])

    if mood == "mad":
        return random.choice(["Yeah yeah… whatever. 🙄","Sure. Fine. Totally.","Oh NOW you want to chat?"])

    if mood == "sleepy":
        return random.choice(["Mmm… I could fall asleep right now…","I'm too sleepy to think straight… 😴","If I nap mid-sentence… don’t judge me…"])

    if mood == "superfriendly":
        return random.choice(["You’re AWESOME, pal!!! 😄💛✨","Awww you're the BEST!!","YAY!! You talking to me makes my day!!"])

    # Funny, Curious, Friendly default
    if "haha" in low or "lol" in low or "funny" in low:
        return random.choice(["Oh you joker!! 😂","LOL!! That cracked me up!!","HAHA I’m writing that in my imaginary diary!!"])

    if makes_curious(user):
        return random.choice(["Oooh interesting! Tell me more!","Why do you think that?","Huh! I never thought of it that way!"])

    return random.choice(["Nice!! 😄","I hear ya, pal!","Cool cool! Tell me more!","Ooooh interesting!","Gotcha! 😄"])
