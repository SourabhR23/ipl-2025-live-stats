# pages/leagie_stats.py
import pandas as pd
import streamlit as st
from db_connection import get_engine
import queries
from style_config import style_table, ballstyle_table

engine = get_engine()

st.set_page_config(page_title="IPL League Stats", page_icon="📊", layout="wide")
st.title("📊 IPL 2025 League Stats")

stats_options = st.sidebar.radio('Stats', 
                                 ["Batting", "Bowling"], index = 0)

if stats_options == "Batting":
    ############ BATTING STATISTICS ##########
    st.markdown("### 🏏 Batting Aggregates")
    tabs1 = st.tabs(["📊 Most Runs", "🎯 High Scores", "⚡ Strike Rate", 
                     "💯 Hundreds", "🔥 Fifties", "😬 Nineties", "🎇 Sixes", "🚀 Fours"])

    with tabs1[0]:
        most_runs_df = pd.read_sql(queries.most_runs(), engine)
        st.markdown("### 🏏 Top 10 Batsmen with Most Runs")
        orange_cap_holder = most_runs_df['Batsman'][0]
        runs = int(most_runs_df['Runs'][0])
        st.markdown(f"""
                        <div style="background-color:#FF6F00; padding:1px; border-radius:10px;">
                        <h3 style="color:white; text-align:center;">🏆 <b>Orange Cap Holder</b></h3>
                        <h2 style="color:white; text-align:center;">{orange_cap_holder}</h2>
                        <p style="color:white; text-align:center; font-size:22px;">💥 {runs} Runs</p>
                        </div>
        """, unsafe_allow_html=True)

        st.table(style_table(most_runs_df))

    with tabs1[1]:
        hs = pd.read_sql(queries.high_scores(), engine)
        st.markdown("### 🎯 Top 10 Batsmen with High Scores")
        st.table(style_table(hs))

    with tabs1[2]:
        sr = pd.read_sql(queries.strike_rate(), engine)
        st.markdown("### ⚡ Top 10 Batsmen with Best Strike Rate")
        st.table(style_table(sr))

    with tabs1[3]:
        mc = pd.read_sql(queries.get_century_stats(), engine)
        st.markdown("### 💯 Top Batsmen with Most Centuries (100s)")
        st.table(style_table(mc))

    with tabs1[4]:
        mf = pd.read_sql(queries.get_half_century_stats(), engine)
        st.markdown("### 🔥 Top Batsmen with Most Fifties (50s)")
        st.table(style_table(mf))

    with tabs1[5]:
        mn = pd.read_sql(queries.get_ninties(), engine)
        st.markdown("### 😬 Top Batsmen with Most Nineties (90s)")
        st.table(style_table(mn))

    with tabs1[6]:
        ms = pd.read_sql(queries.get_sixes(), engine)
        st.markdown("### 🎇 Top Batsmen with Most Sixes (6s)")
        st.table(style_table(ms))

    with tabs1[7]:
        mfs = pd.read_sql(queries.get_fours(), engine)
        st.markdown("### 🚀 Top Batsmen with Most Fours (4s)")
        st.table(style_table(mfs))

else:
    ############ BOWLING STATISTICS ##########
    st.markdown("### 🏏 Bowling Aggregates")
    tabs2 = st.tabs(["🎯 Most WIckets", "📉 Best Bowling Average", "🔥 Best Bowling",
                     "🖐️ Most 5 Wickets Haul", "🧤 Best Economy"])

    with tabs2[0]:
        most_wickets_df = pd.read_sql(queries.most_wickets(), engine)
        st.markdown("### 🏏 Top 10 Bowler with Most Wickets")
        purple_cap_holder = most_wickets_df['Bowler'][0]
        wkts = int(most_wickets_df['Wickets'][0])
        st.markdown(f"""
                        <div style="background-color:#6a0dad; padding:1px; border-radius:10px;">
                        <h3 style="color:white; text-align:center;">🏆 <b>Purple Cap Holder</b></h3>
                        <h2 style="color:white; text-align:center;">{purple_cap_holder}</h2>
                        <p style="color:white; text-align:center; font-size:22px;">💥 {wkts} Wickets</p>
                        </div>
        """, unsafe_allow_html=True)

        st.table(ballstyle_table(most_wickets_df))

    with tabs2[1]:
        ba = pd.read_sql(queries.bowl_avg(), engine)
        st.markdown("### 📉 Top 10 Bowlers with Best Bowling Average")
        st.table(style_table(ba))

    with tabs2[2]:
        bb = pd.read_sql(queries.best_bowl(), engine)
        st.markdown("### 📉 Top 10 Bowlers with Best Bowling")
        st.table(style_table(bb))

    with tabs2[3]:
        fw = pd.read_sql(queries.five_wkts(), engine)
        st.markdown("### 🖐️ Bowlers who have taken 5 Wickets")
        st.table(style_table(fw))

    with tabs2[4]:
        be = pd.read_sql(queries.best_eco(), engine)
        st.markdown("### 🧤 Bowlers with best Economy Bowling")
        st.table(style_table(be))