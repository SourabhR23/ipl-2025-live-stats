import streamlit as st
import pandas as pd
from db_connection import get_engine
import queries
from style_config import scorecard, get_team_color, render_innings, render_cap_holder

# Set page config first
st.set_page_config(page_title="IPL 2025 Dashboard", layout="wide", page_icon="🏏")

# ✅ Apply dark theme styling
st.markdown("""
    <style>
        [data-testid="stDecoration"] { display: none; }
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='background-color:#1f77b4;padding:15px 25px;border-radius:10px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.2); margin-bottom:20px;'>
        <h1 style='color:white;margin:0;'>🏏 IPL 2025 Matches Score Dashboard</h1>
    </div>
""", unsafe_allow_html=True)

# Page title
st.title("🏏 IPL 2025 Matches Score Dashboard")

# Load match list and allow match selection
engine = get_engine()

matches_df = pd.read_sql(queries.get_all_matches(), engine)
match_options = matches_df['match_name'].tolist()
selected_match = st.selectbox("Select Match", match_options)
match_id = matches_df[matches_df['match_name'] == selected_match]['match_id'].values[0]

# Toss summary
toss_winner = matches_df[matches_df['match_name'] == selected_match]['toss_winner'].values[0]
toss_choice = matches_df[matches_df['match_name'] == selected_match]['toss_choice'].values[0]

st.subheader(f"{toss_winner} won the toss and chose to {toss_choice}")
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

# Cap Holders in Sidebar
most_runs_df = pd.read_sql(queries.most_runs(), engine)
orange_cap_holder = most_runs_df['batsman_name'][0]
runs = int(most_runs_df['RUNS'][0])
render_cap_holder("Orange", orange_cap_holder, runs, "#FF6F00", "🧡", "Runs")

most_wks_df = pd.read_sql(queries.most_wickets(), engine)
purple_cap_holder = most_wks_df['Bowler'][0]
wkts = int(most_wks_df['Wickets'][0])
render_cap_holder("Purple", purple_cap_holder, wkts, "#6a0dad", "💜", "Wickets")
