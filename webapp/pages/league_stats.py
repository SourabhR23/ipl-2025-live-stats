# pages/leagie_stats.py
import pandas as pd
import streamlit as st
from db_connection import get_engine
import queries
from style_config import style_table

engine = get_engine()

st.title("📊 IPL 2025 League Stats")

stats_options = st.sidebar.radio('Stats', 
                                 ["Batting", "Bowling"], index = 0)

st.markdown("### 🏏 Batting Aggregates")
tabs1 = st.tabs(["📊 Most Runs", "🎯 High Scores", "⚡ Strike Rate"])

with tabs1[0]:
    most_runs_df = pd.read_sql(queries.most_runs(), engine)
    st.markdown("### 🏏 Top 10 Batsmen with Most Runs")
    st.table(style_table(most_runs_df))

with tabs1[1]:
    hs = pd.read_sql(queries.high_scores(), engine)
    st.markdown("### 🎯 Top 10 Batsmen with High Scores")
    st.table(style_table(hs))

with tabs1[2]:
    sr = pd.read_sql(queries.strike_rate(), engine)
    st.markdown("### ⚡ Top 10 Batsmen with Bets Strike Rate")
    st.table(style_table(sr))


st.markdown("### 💥 Impact Stats")
tabs2 = st.tabs(["💯 Hundreds", "🔥 Fifties", "😬 Nineties"])

with tabs2[0]:
    mc = pd.read_sql(queries.get_century_stats(), engine)
    st.markdown("### 💯 Top Batsmen with Most Centuries (100s)")
    st.table(style_table(mc))

with tabs2[1]:
    mf = pd.read_sql(queries.get_half_century_stats(), engine)
    st.markdown("### 🔥 Top Batsmen with Most Fifties (50s)")
    st.table(style_table(mf))

with tabs2[2]:
    mn = pd.read_sql(queries.get_ninties(), engine)
    st.markdown("### 😬 Top Batsmen with Most Nineties (90s)")
    st.table(style_table(mn))


st.markdown("### 🎯 Boundary Metrics")
tabs3 = st.tabs(["🎇 Sixes", "🚀 Fours"])

with tabs3[0]:
    ms = pd.read_sql(queries.get_sixes(), engine)
    st.markdown("### 🎇 Top Batsmen with Most Sixes (6s)")
    st.table(style_table(ms))

with tabs3[1]:
    mfs = pd.read_sql(queries.get_fours(), engine)
    st.markdown("### 🚀 Top Batsmen with Most Fours (4s)")
    st.table(style_table(mfs))
