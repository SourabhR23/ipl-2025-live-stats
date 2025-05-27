import requests
import os
from dotenv import load_dotenv
from datetime import datetime, time, timedelta
import pytz
import streamlit as st

# Load environment
load_dotenv()
CRIC_API_KEY = os.getenv("CRIC_API_KEY")
BASE_URL = "https://api.cricapi.com/v1/match_scorecard"

# Define refresh slots (IST)
ALLOWED_SLOTS_IST = [
    time(16, 0), time(17, 30), time(19, 0), time(20, 0), 
    time(20, 30), time(21, 30), time(23, 0), time(0, 30)  # Evening + Midnight slots
]

# ✅ Get current IST time
def get_current_ist():
    IST = pytz.timezone("Asia/Kolkata")
    return datetime.now(IST)

# ✅ Get active refresh slot (handles across midnight)
def get_current_slot():
    now = get_current_ist()
    today = now.date()
    ist = pytz.timezone("Asia/Kolkata")

    # Generate datetime slots: today for normal, tomorrow for post-midnight
    slots = []
    for slot in ALLOWED_SLOTS_IST:
        dt_slot = datetime.combine(today, slot)
        if slot < time(1, 0):  # Slot like 00:30 belongs to *next day*
            dt_slot += timedelta(days=1)
        slots.append(ist.localize(dt_slot))

    # Reverse and get the latest eligible slot
    for dt in reversed(slots):
        if now >= dt:
            return dt.strftime("%H:%M")

    return None

# 🔁 Auto-refresh logic (triggered if slot changes)
def auto_refresh_by_slot():
    current_slot = get_current_slot()
    if "last_slot" not in st.session_state:
        st.session_state.last_slot = current_slot
    elif st.session_state.last_slot != current_slot:
        st.session_state.last_slot = current_slot
        st.experimental_rerun()

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
