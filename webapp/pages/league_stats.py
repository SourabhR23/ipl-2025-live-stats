# pages/leagie_stats.py
import pandas as pd
import streamlit as st
from db_connection import get_engine
import queries

engine = get_engine()

st.title("📊 IPL 2025 League Stats")

stats_options = st.sidebar.radio('Stats', 
                                 ["Batting", "Bowling"], index = 0)

if stats_options == "Batting":
    st.subheader("Batting")
    view_option = st.selectbox("Select", ["-- Select Option --", "Most Runs", "High Scores", "Most Hundreds(100s)"])
    if view_option == "Most Runs":
        most_runs = pd.read_sql(queries.most_runs(), engine)
        st.dataframe(most_runs)
    elif view_option == "High Scores":
        most_runs = pd.read_sql(queries.high_scores(), engine)
        st.dataframe(most_runs)
    elif view_option == "Most Hundreds(100s)":
        cent = pd.read_sql(queries.get_century_stats(), engine)
        st.dataframe(cent)


