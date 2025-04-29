import streamlit as st
import pandas as pd
from db_connection import get_engine
import queries

st.set_page_config(page_title="IPL 2025 Dashboard", layout="wide")
st.title("🏏 IPL 2025 Live Dashboard")

engine = get_engine()

matches_df = pd.read_sql(queries.get_all_matches(), engine)
st.dataframe(matches_df)

match_options = matches_df['name'].tolist()
selected_match = st.selectbox("Select Match", match_options)

match_id = matches_df[matches_df['name'] == selected_match]['id'].values[0]

st.subheader("Batting Scorecard")
batting_df = pd.read_sql(queries.get_batting_scorecard(match_id), engine)
st.dataframe(batting_df)

st.subheader("Bowling Scorecard")
bowling_df = pd.read_sql(queries.get_bowling_scorecard(match_id), engine)
st.dataframe(bowling_df)
