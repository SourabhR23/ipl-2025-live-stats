import streamlit as st
import pandas as pd
from db_connection import get_engine
import queries
from style_config import scorecard, get_team_color, render_innings

# Set page config first
st.set_page_config(page_title="IPL 2025 Dashboard", layout="wide", page_icon="🏏")

# ✅ Apply dark theme styling
st.markdown("""
    <style>
        .main { background-color: #0e1117; color: white; }
        h1, h2, h3, h4, h5 { color: #f0f0f0; }
        .stMetric { text-align: center; }
        .stDataFrame { border-radius: 12px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# Page title
st.title("🏏 IPL 2025 Matches Score Dashboard")

# Load match list and allow match selection
engine = get_engine()

matches_df = pd.read_sql(queries.get_all_matches(), engine)
match_options = matches_df['match_name'].tolist()
selected_match = st.selectbox("Select Match", match_options)
match_id = matches_df[matches_df['match_name'] == selected_match]['match_id'].values[0]

# Get match summary for 2 innings
innings_df = pd.read_sql(queries.get_innings_details(match_id), engine)

# Show scorecard-style summary
col1, col2 = st.columns(2)
with col1:
    st.markdown(scorecard(
                    innings_df['inning_name'][0], 
                    innings_df['runs'][0], 
                    innings_df['wickets'][0], 
                    innings_df['overs'][0], 
                    get_team_color(innings_df['inning_name'][0])), 
                    unsafe_allow_html=True)

with col2:
    st.markdown(scorecard(
                    innings_df['inning_name'][1], 
                    innings_df['runs'][1], 
                    innings_df['wickets'][1], 
                    innings_df['overs'][1], 
                    get_team_color(innings_df['inning_name'][1])), 
                    unsafe_allow_html=True)

# Match result
st.markdown("---")
st.success(f"🏆 {matches_df[matches_df['match_name'] == selected_match]['status'].values[0]}")


# Load batting and bowling data
batting_df = pd.read_sql(queries.get_batting_scorecard(match_id), engine)
bowling_df = pd.read_sql(queries.get_bowling_scorecard(match_id), engine)
innings = batting_df['inning_name'].unique()

# Render innings with highlight and styled tables
st.subheader(" Innings Scoreboard ")
st.markdown("___")

# ✅ Innings 1
st.markdown("Innings 1")
render_innings(
    innings_name=innings[0],
    bat_df=batting_df[batting_df['inning_name'] == innings[0]].reset_index(drop=True),
    bowl_df=bowling_df[bowling_df['inning_name'] == innings[0]].reset_index(drop=True),
    opponent_name=innings[1]
)


# ✅ Innings 2
st.markdown("Innings 2")
render_innings(
    innings_name=innings[1],
    bat_df=batting_df[batting_df['inning_name'] == innings[1]].reset_index(drop=True),
    bowl_df=bowling_df[bowling_df['inning_name'] == innings[1]].reset_index(drop=True),
    opponent_name=innings[0]
)


