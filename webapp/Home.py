import streamlit as st
import pandas as pd
from datetime import datetime
from db_connection import get_engine
import queries
from style_config import *
from live_api import get_live_data, can_call_api
from pytz import timezone

IST = timezone("Asia/Kolkata")
current_ist = datetime.now(IST)

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
        st.metric("✅ Match Today", "Live Score:")

        for idx, row in today_matches.iterrows():
            match_id = row['id']
            with st.expander(f"🕹️ {row['name']}"):
                st.markdown(f"📍 **Venue:** _{row['venue']}_")
                st.caption("🕒 Scores last updated from CricAPI (Max 5 API hits/day).")

                if can_call_api():
                    live_data = get_live_data(match_id)
                    st.caption(f"✅ Fetched live at {current_ist.strftime('%I:%M %p IST')}")
                else:
                    st.warning("⚠️ Live fetch blocked (limit reached or outside match time).")
                    live_data = None

                if live_data:
                    # 🔄 Extract and display match status
                    match_status = live_data.get('status', 'Unknown')
                    st.markdown(f"""
                        <div style="background-color:#444;padding:8px 16px;border-radius:8px;display:inline-block;margin-bottom:10px;">
                            <span style="color:white;font-weight:bold;">📣 Status: {match_status}</span>
                        </div>
                    """, unsafe_allow_html=True)

                    if 'score' in live_data:
                        col1, col2 = st.columns(2)
                        for i, inning in enumerate(live_data['score']):
                            team = inning.get('inning', 'N/A').rsplit(' Inning', 1)[0]
                            runs = inning.get('r', 0)
                            wickets = inning.get('w', 0)
                            overs = inning.get('o', 0)

                            with [col1, col2][i % 2]:
                                st.markdown(f'''
                                    <div style="background-color:#222;padding:16px;border-radius:10px;margin-bottom:10px;">
                                        <h3 style="color:white;">{team}</h3>
                                        <p style="color:white;font-size:20px;"><b>{runs}/{wickets}</b> in {overs} overs</p>
                                    </div>
                                ''', unsafe_allow_html=True)
                    else:
                        st.info("Live score not available yet.")
                else:
                    st.info("Match has not started or data unavailable.")

# Cap Holders in Sidebar
most_runs_df = pd.read_sql(queries.most_runs(), engine)
orange_cap_holder = most_runs_df['Batsman'][0]
runs = int(most_runs_df['Runs'][0])
team = most_runs_df['Team'][0]
render_cap_holder("Orange", orange_cap_holder, team, runs, "#FF6F00", "🧡", "Runs")

most_wks_df = pd.read_sql(queries.most_wickets(), engine)
purple_cap_holder = most_wks_df['Bowler'][0]
wkts = int(most_wks_df['Wickets'][0])
team = most_wks_df['Team'][0]
render_cap_holder("Purple", purple_cap_holder, team, wkts, "#6a0dad", "💜", "Wickets")

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
