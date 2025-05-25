import streamlit as st
import pandas as pd
import ast
from db_connection import get_engine
import queries
from live_api import get_current_ist
from fantasy11_generator import generate_fantasy_xi_for_match
from style_config import style_table, render_logo_and_title

st.set_page_config(page_title="Fantasy XI", layout="wide")
render_logo_and_title("🌟 Fantasy XI for Today's Matches")

engine = get_engine()

# Load match data from IPL_Match_List
all_matches = pd.read_sql(queries.get_live_match(), engine)

# Parse match_date and filter for today
all_matches['match_date'] = pd.to_datetime(all_matches['match_date'], errors='coerce').dt.date
today = get_current_ist().date()
today_matches = all_matches[all_matches['match_date'] == today]

if today_matches.empty:
    st.warning("⚠️ No match found for today.")
    st.stop()

# Extract team1 and team2 from string-formatted 'teams' column
def extract_teams(team_str):
    try:
        teams = ast.literal_eval(team_str)
        if isinstance(teams, list) and len(teams) == 2:
            return pd.Series({'team1': teams[0], 'team2': teams[1]})
    except:
        pass
    return pd.Series({'team1': None, 'team2': None})

team_info = today_matches['teams'].apply(extract_teams)
today_matches = pd.concat([today_matches, team_info], axis=1)

# Strategy Options
st.sidebar.markdown("## 🎯 Strategy Options")
recent_n = st.sidebar.slider("Past Matches to Consider", 1, 5, 3)
strategy = st.sidebar.radio("Team Strategy", ["balanced", "batting", "bowling"])

# Disclaimer
st.sidebar.markdown("### ⚠️ Disclaimer")
st.sidebar.info("Fantasy XI teams shown here are for educational and analytical use only. Not for real money contests.")


# Loop through today’s matches
for i, row in today_matches.iterrows():
    team1, team2 = row['team1'], row['team2']
    match_title = f"{team1} vs {team2}"

    st.markdown(f"## 🏏 Match: {match_title}")
    dream_xi = generate_fantasy_xi_for_match(team1, team2, recent_n, strategy, engine)

    st.markdown(f"### 🌟 Fantasy XI for **{match_title}** ({strategy.capitalize()} Strategy)")
    st.dataframe(style_table(dream_xi), use_container_width=True, hide_index=True)
    st.markdown("---")


st.markdown("""
<div style="background-color:#1e1e1e; padding:16px; border-left: 5px solid #f39c12; border-radius: 8px; margin-bottom: 20px;">
    <h4 style="color:#f1c40f;">📢 Disclaimer</h4>
    <p style="color:white; font-size:14px; line-height:1.6;">
        <strong>We do not promote or encourage real-money gambling or betting of any kind.</strong><br><br>
        Users are advised not to use these suggestions for any commercial fantasy sports platforms.
        The creators of this app bear no responsibility for any financial or legal outcomes arising from the misuse of this information.<br><br>
        Always play responsibly. Participation in fantasy sports should be done in accordance with the laws and regulations applicable in your region.
    </p>
</div>
""", unsafe_allow_html=True)
