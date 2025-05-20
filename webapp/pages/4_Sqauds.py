import pandas as pd
import streamlit as st
from db_connection import get_engine
import squad_queries
from style_config import style_table, ballstyle_table

engine = get_engine()

st.set_page_config(page_title="IPL League Squads", page_icon="📊", layout="wide")

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

st.title("League Squads")

# Team List
TEAMS = ["Select Team"] + ["Kolkata Knight Riders", "Mumbai Indians", "Chennai Super Kings", "Royal Challengers Bengaluru", 
         "Delhi Capitals","Rajasthan Royals", "Gujarat Titans", "Sunrisers Hyderabad", "Lucknow Super Giants", "Punjab Kings"]

# Sidebar filter for nationality
country_filter = st.sidebar.radio(
    "🌍 Filter Players By",
    options=["All", "India", "Overseas"],
    index=0
)

# Select Team
selected_team = st.selectbox("🏏 Choose your IPL Team", TEAMS, index=0)
if selected_team != "Select Team":
    st.markdown(f"### 🧢 Squad for **{selected_team}**")

    # Fetch Squad
    squad = pd.read_sql(squad_queries.squad_tb(selected_team), con=engine)

    # Apply country filter
    if country_filter == "India":
        squad = squad[squad['country'] == 'India']
    elif country_filter == "Overseas":
        squad = squad[squad['country'] != 'India']
    
    # Normalize roles to simplify grouping
    squad['role'] = squad['role'].str.lower()

    # Define role categories
    categories = { 
        'WK-Batsman': ['wk-batsman'],
        'Batsmen': ['batsman'],
        'All-rounders': ['allrounder', 'batting allrounder', 'bowling allrounder'],
        'Bowlers': ['bowler']
    }

    # Display each section
    for section, keywords in categories.items():
        filtered = squad[squad['role'].apply(lambda r: any(k in r for k in keywords))]

        if not filtered.empty:
            with st.expander(f"👥 {section} ({len(filtered)})", expanded=True):
                st.dataframe(
                    filtered[['playerName', 'role', 'battingStyle', 'bowlingStyle', 'country']],
                    hide_index=True
                )
else:
    st.info("Please select a team from the dropdown above.")


