import streamlit as st
import pandas as pd
from db_connection import get_engine
import queries
from style_config import scorecard, get_team_color, get_team_logo_path, render_innings, render_cap_holder

# Set page config first
st.set_page_config(page_title="IPL 2025 Dashboard", layout="wide", page_icon="🏏")

# ✅ Apply dark theme styling
st.markdown("""
    <style>
        /* 🎨 Dark theme styles */
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
venue = matches_df[matches_df['match_name'] == selected_match]['venue'].values[0]
date =  matches_df[matches_df['match_name'] == selected_match]['date'].values[0]

# Toss summary (safe null handling)
toss_winner = matches_df[matches_df['match_name'] == selected_match]['toss_winner'].values[0]
toss_choice = matches_df[matches_df['match_name'] == selected_match]['toss_choice'].values[0]

# Handle missing toss information
if pd.isna(toss_winner) or pd.isna(toss_choice):
    st.subheader("🎲 Toss did not happen or match was abandoned.")
else:
    st.subheader(f"🎲 {toss_winner} won the toss and chose to **{toss_choice.upper()}**")

# Stylish Venue and Date Display
st.markdown(f"""
<div style="background-color:#111827; padding:15px; border-radius:12px; color:white; font-size:16px">
    📍 <b>Venue:</b> {venue}<br>
    📅 <b>Date:</b> {pd.to_datetime(date).strftime('%B %d, %Y')}
</div>
""", unsafe_allow_html=True)

# Get match summary for 2 innings
innings_df = pd.read_sql(queries.get_innings_details(match_id), engine)

# Show scorecard-style summary
team1 = matches_df[matches_df['match_name'] == selected_match]['team1'].values[0]
team2 = matches_df[matches_df['match_name'] == selected_match]['team2'].values[0]

with st.container():
    spacer1, col1, col2, spacer2 = st.columns([0.1, 1, 1, 0.1])
    
    if len(innings_df) >= 1:
        team1 = innings_df['inning_name'][0]
        with col1:
            st.markdown(scorecard(
                team1,
                innings_df['runs'][0],
                innings_df['wickets'][0],
                innings_df['overs'][0],
                get_team_color(team1),
                get_team_logo_path(team1)
            ), unsafe_allow_html=True)

    if len(innings_df) >= 2:
        team2 = innings_df['inning_name'][1]
        with col2:
            st.markdown(scorecard(
                team2,
                innings_df['runs'][1],
                innings_df['wickets'][1],
                innings_df['overs'][1],
                get_team_color(team2),
                get_team_logo_path(team2)
            ), unsafe_allow_html=True)
    else:
        with col2:
            st.markdown("""
                <div style='background-color: #2c2c2c; padding: 20px; border-radius: 10px; text-align: center color: black;;'>
                    <h4>⚠️ Second Innings Not Played</h4>
                    <p>The match was interrupted due to rain or ended prematurely.</p>
                </div>
            """, unsafe_allow_html=True)


# Match result
match_status = matches_df[matches_df['match_name'] == selected_match]['status'].values[0]
if "cancelled" in match_status.lower() or "no result" in match_status.lower():
    st.markdown("""
            <div style='margin-top: 20px; padding: 20px; background-color: brown; border-left: 5px solid green; border-radius: 5px;'>
                <strong>Match Status:</strong> 🌧️ {status}
            </div>
    """.format(status=match_status), unsafe_allow_html=True)
else:
    st.markdown("---")
    st.success(f"🏆 {matches_df[matches_df['match_name'] == selected_match]['status'].values[0]}")


# Load batting and bowling data
batting_df = pd.read_sql(queries.get_batting_scorecard(match_id), engine)
bowling_df = pd.read_sql(queries.get_bowling_scorecard(match_id), engine)

# Render innings with highlight and styled tables
st.subheader(" Innings Scoreboard ")
st.markdown("___")


# 2. Render innings-wise detailed batting & bowling tables
for i in range(len(innings_df)):
    innings_name = innings_df['inning_name'][i]
    team_name = innings_name.split(' Inning')[0]
    
    # Get opponent team from innings_df or match table
    opponent_name = innings_df['inning_name'][1 - i].split(' Inning')[0] if len(innings_df) > 1 else team2


    
    # Filter batting and bowling data for this innings
    bat_df = batting_df[batting_df['inning_name'] == innings_name]
    bowl_df = bowling_df[bowling_df['inning_name'] == innings_name]

    render_innings(team_name, bat_df, bowl_df, opponent_name)


