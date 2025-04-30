import streamlit as st
import pandas as pd
from db_connection import get_engine
import queries

################ HEADER ##################
st.set_page_config(page_title="IPL 2025 Dashboard", layout="wide")
st.title("🏏 IPL 2025 Matches Score Dashboard")

engine = get_engine()

matches_df = pd.read_sql(queries.get_all_matches(), engine)
st.dataframe(matches_df.iloc[:,1:])

match_options = matches_df['match_name'].tolist()
selected_match = st.selectbox("Select Match", match_options)

match_id = matches_df[matches_df['match_name'] == selected_match]['match_id'].values[0]

################ BATTING INFORMATION ##################
st.subheader("Batting Scorecard")
batting_df = pd.read_sql(queries.get_batting_scorecard(match_id), engine)
innings = batting_df['inning_name'].unique()
t1 = innings[0].replace(" Inning 1", "")
t2 = innings[1].replace(" Inning 1", "")

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Team 1: {t1}")
    df1 = batting_df[batting_df['inning_name'] == innings[0]].reset_index(drop=True)
    st.dataframe(df1.iloc[:,1:])
with col2:
    st.subheader(f"Team 2: {t2}")
    df2 = batting_df[batting_df['inning_name'] == innings[1]].reset_index(drop=True)
    st.dataframe(df2.iloc[:,1:])


################ BOWLING INFORMATION ##################
st.subheader("Bowling Scorecard")
bowling_df = pd.read_sql(queries.get_bowling_scorecard(match_id), engine)
innings = bowling_df['inning_name'].unique()

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Team 1: {t1}")
    df1 = bowling_df[bowling_df['inning_name'] == innings[1]].reset_index(drop=True)
    st.dataframe(df1.iloc[:,1:])
with col2:
    st.subheader(f"Team 2: {t2}")
    df2 = bowling_df[bowling_df['inning_name'] == innings[0]].reset_index(drop=True)
    st.dataframe(df2.iloc[:,1:])
