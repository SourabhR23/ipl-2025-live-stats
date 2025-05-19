import requests
import os
from dotenv import load_dotenv
from datetime import datetime, time
import pytz
import streamlit as st

# Load environment
load_dotenv()
CRIC_API_KEY = os.getenv("CRIC_API_KEY")
BASE_URL = "https://api.cricapi.com/v1/match_scorecard"

# Define refresh slots (IST)
ALLOWED_SLOTS_IST = [
    time(16, 0), time(17, 30), time(19, 0), time(20, 30),  # Weekend Match 1
    time(20, 0), time(21, 30), time(23, 0), time(0, 30)    # Common Evening Slots
]

# ✅ Get current IST time
def get_current_ist():
    IST = pytz.timezone("Asia/Kolkata")
    return datetime.now(IST)

# ✅ Get active refresh slot (if now >= slot)
def get_current_slot():
    now = get_current_ist()
    current_time = now.time()
    for slot in reversed(ALLOWED_SLOTS_IST):
        if current_time >= slot:
            return slot.strftime("%H:%M")  # Returns '20:00', '21:30', etc.
    return None

# ✅ Cache per (match_id + slot_key) to limit API hits
@st.cache_data
def get_live_data_scheduled(match_id, slot_key):
    """Fetches live match data and caches per slot."""
    try:
        params = {"apikey": CRIC_API_KEY, "id": match_id}
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("data")
            else:
                st.warning("❌ CricAPI returned an unsuccessful status.")
        else:
            st.error(f"❌ API error: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Exception while calling CricAPI: {e}")
    return None
