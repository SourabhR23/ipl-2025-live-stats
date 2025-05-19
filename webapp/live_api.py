import requests
import streamlit as st
import os
from dotenv import load_dotenv
import json
from datetime import datetime, time
import pytz

# Log the score data
CALL_LOG_FILE = "api_call_log.json"

def get_current_ist():
    IST = pytz.timezone("Asia/Kolkata")
    return datetime.now(IST)

# Connect to API
load_dotenv()
CRIC_API_KEY = os.getenv("CRIC_API_KEY")
BASE_URL = "https://api.cricapi.com/v1/match_scorecard"

# Check match time for refreshing the live scoreboard
def is_match_time():
    now = get_current_ist()
    today = now.weekday()  # Sunday=6
    current_time = now.time()

    if today == 6:
        # Sunday: 3:30–8:00 PM or 7:00–12:00 AM
        return (time(15, 30) <= current_time <= time(20, 0)) or \
               (time(19, 0) <= current_time <= time(23, 59))
    else:
        # Weekdays: 7:00–12:00 AM
        return time(19, 0) <= current_time <= time(23, 59)

# Connect to API during match only
def can_call_api():
    if not os.path.exists(CALL_LOG_FILE):
        with open(CALL_LOG_FILE, "w") as f:
            json.dump({}, f)

    with open(CALL_LOG_FILE, "r") as f:
        log = json.load(f)

    today_str = datetime.today().strftime("%Y-%m-%d")
    calls_today = log.get(today_str, 0)

    if calls_today < 5 and is_match_time():
        # Update log with new count
        log[today_str] = calls_today + 1
        with open(CALL_LOG_FILE, "w") as f:
            json.dump(log, f)
        return True
    return False

# Get live data
@st.cache_data(ttl=5400)
def get_live_data(match_id):
    try:
        params = {"apikey": CRIC_API_KEY, "id": match_id}
        response = requests.get(BASE_URL, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("data")
            else:
                st.warning("❌ CricAPI status not success")
        else:
            st.error(f"❌ API error: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Exception: {e}")
    return None

def reset_api_log_if_needed():
    today_str = get_current_ist().strftime("%Y-%m-%d")
    
    if not os.path.exists(CALL_LOG_FILE):
        return

    with open(CALL_LOG_FILE, "r") as f:
        try:
            log = json.load(f)
        except json.JSONDecodeError:
            log = {}

    # Keep only today's entry
    updated_log = {today_str: log.get(today_str, 0)}
    
    with open(CALL_LOG_FILE, "w") as f:
        json.dump(updated_log, f)
