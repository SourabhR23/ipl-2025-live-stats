import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db_connection import get_engine
from style_config import style_table, render_logo_and_title, get_team_color
import queries

# Setup
st.set_page_config(page_title="Head to Head", layout="wide")
render_logo_and_title("🤝 Head-to-Head Team Comparison")

engine = get_engine()
matches = pd.read_sql(queries.get_all_matches(), engine)
teams = sorted(matches['team1'].unique())

# Team Selectors
col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox("🏏 Select Team A", teams)
with col2:
    team2 = st.selectbox("🏏 Select Team B", [t for t in teams if t != team1])

if team1 and team2:
    st.markdown("----")

    # Filter matches between team1 and team2
    h2h_matches = matches[((matches['team1'] == team1) & (matches['team2'] == team2)) |
                          ((matches['team1'] == team2) & (matches['team2'] == team1))]

    st.markdown(f"### 📜 Match Summary: {len(h2h_matches)} matches played")

    # Win Count
    wins_team1 = h2h_matches[h2h_matches['match_winner'] == team1].shape[0]
    wins_team2 = h2h_matches[h2h_matches['match_winner'] == team2].shape[0]
    no_results = h2h_matches[h2h_matches['match_winner'].isnull()].shape[0]

    st.markdown("#### 🏆 Win Summary")
    st.info(f"{team1}: **{wins_team1} Wins** | {team2}: **{wins_team2} Wins** | No Result: {no_results}")

    # Recent 5 Matches Table
    st.markdown("### 🔙 Last Encounters")
    recent = h2h_matches.sort_values(by='date', ascending=False).head(5)[
        ['match_name', 'venue', 'date', 'match_winner', 'status']]
    st.dataframe(style_table(recent), use_container_width=True, hide_index=True)

    # Average Score Comparison
    innings = pd.read_sql(queries.inn(), engine)
    h2h_ids = h2h_matches['match_id'].tolist()
    if len(h2h_ids) == 1:
        match_id_clause = f"('{h2h_ids[0]}')"  # no comma
    else:
        match_id_clause = str(tuple(h2h_ids))
    h2h_innings = innings[innings['match_id'].isin(h2h_ids)]

    avg_scores = h2h_innings[h2h_innings['team'].isin([team1, team2])].groupby('team')['runs'].mean().reset_index()
    avg_scores.columns = ['Team', 'Avg Runs']

    # Avg Runs Chart
    fig1, ax1 = plt.subplots(figsize=(5, 3))
    bars1 = ax1.bar(avg_scores['Team'], avg_scores['Avg Runs'], color=['#FFAD33', '#66CCFF'])

    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval:.1f}", ha='center', va='bottom', fontsize=5, color='white')

    ax1.set_title("📈 Avg Runs in H2H", fontsize=7, color='white')
    ax1.set_ylabel("Runs", color='white')
    ax1.tick_params(colors='white')
    ax1.set_facecolor('#1e1e1e')
    fig1.patch.set_facecolor('#0e1117')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    st.pyplot(fig1)
    
    # Top Batting Performers
    with col1:
        top_batsmen = pd.read_sql(queries.top_batsmen_query(match_id_clause), engine)
        st.markdown("### 🔥 Top Batting Performers")
        st.dataframe(
            style_table(top_batsmen),
            use_container_width=False,
            width=480,
            hide_index=True
        )

    # Top Bowling Performers
    with col2:
        top_bowlers = pd.read_sql(queries.top_bowlers_query(match_id_clause), engine)
        st.markdown("### 🎯 Top Bowling Performers")
        st.dataframe(
            style_table(top_bowlers),
            use_container_width=False,
            width=480,
            hide_index=True
        )

    # Toss Insights
    st.markdown("### 🎲 Toss Wins and Choices")
    toss_summary = h2h_matches.groupby(['toss_winner', 'toss_choice']).size().reset_index(name='Count')
    st.dataframe(style_table(toss_summary), use_container_width=True, hide_index=True)

    # Venue Distribution
    st.markdown("### 🏟️ Venues Played")
    venue_counts = h2h_matches['venue'].value_counts().reset_index()
    venue_counts.columns = ['Venue', 'Matches']
    st.dataframe(style_table(venue_counts), use_container_width=True, hide_index=True)
