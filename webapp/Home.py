import streamlit as st
import pandas as pd
from datetime import datetime
from db_connection import get_engine
import queries
from style_config import *


# Load data
engine = get_engine()
matches_df = pd.read_sql(queries.get_all_matches(), engine)

# Set page configuration
st.set_page_config(page_title="🏏 IPL 2025 Dashboard", layout="wide", page_icon="🏆")

# Apply page theme styles
st.markdown("""
    <style>
        .main { background-color: #0e1117; }
        h1, h2, h3, h4, h5, h6, p { color: white; }
        .stDataFrame, .stMetric, .element-container { border-radius: 12px !important; }
    </style>
""", unsafe_allow_html=True)

# --- Render Title ---
render_logo_and_title("IPL 2025 Live Dashboard")

# Load match data
matches_df = pd.read_sql(queries.get_all_matches(), engine)
all_matches = pd.read_sql(queries.get_live_match(), engine)

# Convert date column to datetime if not already
all_matches['match_date'] = pd.to_datetime(all_matches['match_date']).dt.date

# Get today's date
today = datetime.today().date()

# Filter matches happening today
today_matches = all_matches[all_matches['match_date'] == today]

# Key Stats
st.markdown("### 📊 Quick Stats")
col1, col2 = st.columns([1, 3])

with col1:
    col1.metric("🕹️ TOTAL MATCHES COMPLETED:", len(matches_df))

with col2:
    if not today_matches.empty:
        st.metric("✅ Match Today", f"{len(today_matches)} Matches")

        for idx, row in today_matches.iterrows():
            with st.expander(f"🕹️ {row['name']}"):
                st.markdown(f"📍 Venue: _{row['venue']}_")
    else:
        st.metric("❌ No Match Today", "")
        st.write("Enjoy the break 😄")

# Cap Holders in Sidebar
most_runs_df = pd.read_sql(queries.most_runs(), engine)
orange_cap_holder = most_runs_df['Batsman'][0]
runs = int(most_runs_df['Runs'][0])
render_cap_holder("Orange", orange_cap_holder, runs, "#FF6F00", "🧡", "Runs")

most_wks_df = pd.read_sql(queries.most_wickets(), engine)
purple_cap_holder = most_wks_df['Bowler'][0]
wkts = int(most_wks_df['Wickets'][0])
render_cap_holder("Purple", purple_cap_holder, wkts, "#6a0dad", "💜", "Wickets")

st.markdown("---")

# Team Logos Display
st.markdown("### 🏏 Participating Teams")
render_team_grid()

st.markdown("---")

# Feature Panels
st.markdown("### 🚀 Explore Dashboard Features")

left, mid, right = st.columns(3)

with left:
    st.markdown("#### 📋 Match Scoreboard")
    st.markdown("View live or past match scorecards with batting & bowling breakdowns.")
    st.image("https://img.icons8.com/external-konkapp-outline-color-konkapp/64/external-scoreboard-soccer-konkapp-outline-color-konkapp.png", 
             width=60)

with mid:
    st.markdown("#### 📊 League Stats")
    st.markdown("Check out league leaders: runs, wickets, averages, 5-fers, and more.")
    st.image("https://img.icons8.com/external-kiranshastry-lineal-color-kiranshastry/64/external-analytics-business-kiranshastry-lineal-color-kiranshastry-2.png", 
             width=60)

with right:
    st.markdown("#### 📈 Points Table")
    st.markdown("Track team standings, net run rate, wins/losses and form.")
    st.image("https://img.icons8.com/external-filled-line-andi-nur-abdillah/64/external-Leaderboard-gaming-(filled-line)-filled-line-andi-nur-abdillah.png", 
             width=60)

st.markdown("---")

# Footer
st.markdown("<p style='text-align: center; color: #888;'>Built with ❤️ using Streamlit | Data source: CricAPI | IPL 2025</p>", unsafe_allow_html=True)
