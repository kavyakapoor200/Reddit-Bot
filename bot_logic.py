# bot_logic.py
import time
from datetime import datetime, timedelta
import pytz
import os
import praw
import requests
import json
import re
from dotenv import load_dotenv
import os


# === Mistral 7B Setup ===
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

# === Reddit Setup ===
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent="script:BotPo:v1"
)

# SAME SUBREDDITS + ACTIVE HOURS
subreddits = {
    "r/algotrading": {"instruction": "Focus on practical bot-building advice and community sharing.", "active_hours": (9, 15)},
    "r/quant": {"instruction": "Relate to mathematical modeling or statistical strategy design.", "active_hours": (19, 2)},
    "r/QuantFinance": {"instruction": "Finance bot stuff", "active_hours": (19, 2)},
    "r/HighFrequencyTrading": {"instruction": "Low latency stuff", "active_hours": (20, 3)},
    "r/Python": {"instruction": "Python learning", "active_hours": (10, 18)},
    "r/learnpython": {"instruction": "Beginner friendly", "active_hours": (11, 17)},
    "r/Backtesting": {"instruction": "Data testing", "active_hours": (9, 12)},
    "r/AlgoTradingIndia": {"instruction": "Indian markets", "active_hours": (9, 15)},
    "r/TradeBots": {"instruction": "Automation logic", "active_hours": (15, 20)},
    "r/NSEbets": {"instruction": "Casual India trading", "active_hours": (10, 16)}
}

# === Load cooldown ===
LAST_POSTED_FILE = "last_posted.json"
try:
    with open(LAST_POSTED_FILE, "r") as f:
        last_posted = {sr: datetime.fromisoformat(t) for sr, t in json.load(f).items()}
except:
    last_posted = {}

def get_current_ist_time():
    return datetime.now(pytz.timezone('Asia/Kolkata'))

def is_within_active_hours(start, end, hour):
    return start <= hour < end if start <= end else (hour >= start or hour < end)

def can_post(subreddit):
    now = get_current_ist_time()
    hour = now.hour
    start, end = subreddits[subreddit]["active_hours"]
    last_time = last_posted.get(subreddit)
    return is_within_active_hours(start, end, hour) and (last_time is None or (now - last_time) >= timedelta(hours=1))

def update_last_posted(subreddit):
    last_posted[subreddit] = get_current_ist_time()
    with open(LAST_POSTED_FILE, "w") as f:
        json.dump({sr: t.isoformat() for sr, t in last_posted.items()}, f)

def clean_output(text):
    return re.sub(r'\[\d+\]', "", text)

# === Mistral Call Function ===
def call_mistral(prompt):
    payload = {
        "model": "mistral-7b-instruct",  # <-- Change to your model if needed
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        r = requests.post(MISTRAL_URL, json=payload, headers=HEADERS)
        return clean_output(r.json()['choices'][0]['message']['content'])
    except Exception as e:
        return f"Error: {e}"

# === Strategy Based ===
def generate_from_strategy(strategy):
    sr = call_mistral(f"Best Indian subreddit for: {strategy}").split()[0]
    title = call_mistral(f"Write a short Reddit title for: {strategy}").splitlines()[0]
    body = call_mistral(f"Write a 60-word Reddit post for: {strategy}")
    return sr, title, body

# === Fallback ===
def generate_fallback_post(subreddit, instruction):
    topic = call_mistral(f"Topic for {subreddit}, instruction: {instruction}")
    title = call_mistral(f"Write title for: {topic}").splitlines()[0]
    body = call_mistral(f"Write post for: {topic}")
    return title, body

# === Submit to Reddit ===
def post_to_subreddit(subreddit, title, body, force=False):
    if not force and not can_post(subreddit):
        return f"Cooldown/Inactive: {subreddit}"

    sr = reddit.subreddit(subreddit.replace("r/", ""))
    submission = sr.submit(title=title, selftext=body)
    update_last_posted(subreddit)
    return f"Posted to {subreddit}"
