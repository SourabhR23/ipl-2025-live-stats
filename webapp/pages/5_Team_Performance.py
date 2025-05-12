import streamlit as st
import pandas as pd
from db_connection import get_engine
import squad_queries
from style_config import style_table, ballstyle_table

st.set_page_config(page_title="Team Performance Insights", layout="wide")
st.title("📊 Team Performance Breakdown")

# Load match list and allow match selection
engine = get_engine()

squad_df = pd.read_sql(squad_queries.all_squad(), engine)
batting_df = pd.read_sql(squad_queries.all_batting(), engine)
bowling_df = pd.read_sql(squad_queries.all_bowling(), engine)

# Team selection
selected_team = st.selectbox("🏏 Select a Team", squad_df['teamName'].unique())

# Filter Data
team_squad = squad_df[squad_df['teamName'] == selected_team]
team_batting = batting_df[batting_df['batsman_id'].isin(team_squad['playerId'])]
team_bowling = bowling_df[bowling_df['bowler_id'].isin(team_squad['playerId'])]

# Display Team Logo
team_logo = team_squad['teamImg'].iloc[0]
st.image(team_logo, width=80)

# Batting Performance
batting_stats = team_batting.groupby(['batsman_name']).agg({
    'runs': 'sum',
    'balls': 'sum',
    'fours': 'sum',
    'sixes': 'sum'
}).reset_index()
batting_stats['Strike Rate'] = (batting_stats['runs'] / batting_stats['balls']) * 100
batting_stats = batting_stats.sort_values(by='runs', ascending=False)

# Bowling Performance
bowling_stats = team_bowling.groupby(['bowler_name']).agg({
    'overs': 'sum',
    'runs_conceded': 'sum',
    'wickets': 'sum',
    'economy': 'mean'
}).reset_index()
bowling_stats = bowling_stats.sort_values(by='wickets', ascending=False)

# Player Impact
# Normalize both names to ensure accurate merge
batting_stats['Player'] = batting_stats['batsman_name'].str.strip()
bowling_stats['Player'] = bowling_stats['bowler_name'].str.strip()

# Merge on 'Player'
impact_df = pd.merge(
    batting_stats[['Player', 'runs']],
    bowling_stats[['Player', 'wickets']],
    on='Player',
    how='outer'
).fillna(0)

impact_df['Impact Score'] = impact_df['runs'] + (impact_df['wickets'] * 20)
impact_df = impact_df[['Player', 'runs', 'wickets', 'Impact Score']]
impact_df = impact_df.sort_values(by='Impact Score', ascending=False)

# Tabs UI
st.markdown("---")
tab1, tab2, tab3, tab4 = st.tabs(["📋 Squad", "🏏 Batting", "🎯 Bowling", "🌟 Impact"])

with tab1:
    st.subheader("🧢 Squad Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Composition by Role**")
        st.dataframe(team_squad['role'].value_counts().reset_index().rename(columns={'index': 'Role', 'role': 'Count'}))
    with col2:
        st.markdown("**Nationality Breakdown**")
        st.dataframe(team_squad['country'].value_counts().reset_index().rename(columns={'index': 'Country', 'country': 'Count'}))

with tab2:
    st.subheader("🏏 Batting Performance")
    st.dataframe(style_table(batting_stats.iloc[:, :-1]), use_container_width=True, hide_index=True)
    st.markdown("### 🔝 Top Run Scorers")
    st.bar_chart(batting_stats.set_index('Player')['runs'].head(5))

with tab3:
    st.subheader("🎯 Bowling Performance")
    st.dataframe(ballstyle_table(bowling_stats.iloc[:, :-1]), use_container_width=True, hide_index=True)
    st.markdown("### 🔝 Top Wicket-Takers")
    st.bar_chart(bowling_stats.set_index('Player')['wickets'].head(5))

with tab4:
    st.subheader("🌟 Player Impact Summary")
    st.dataframe(style_table(impact_df), use_container_width=True, hide_index=True)

    # Highlight MVP
    if not impact_df.empty:
        top_player = impact_df.iloc[0]
        st.success(f"🏆 MVP: **{top_player['Player']}** with an Impact Score of **{top_player['Impact Score']}**")
