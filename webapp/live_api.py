import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
CRIC_API_KEY = st.secrets["CRIC_API_KEY"]
BASE_URL = "https://api.cricapi.com/v1/match_scorecard"


@st.cache_data(ttl=10800)
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
