import pandas as pd
import streamlit as st
from db_connection import get_engine
import queries
from style_config import style_table, ballstyle_table

engine = get_engine()

st.set_page_config(page_title="Fielding & Extras Stats", page_icon="📊", layout="wide")

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

st.title("📊 Fielding & Extras Stats")

stats_options = st.sidebar.radio('Stats', 
                                 ["Fielding", "Extras"], index = 0)

if stats_options == "Fielding":
    ############ FIELDING STATISTICS ##########
    st.markdown("### 🏏 Fielding Aggregates")
    tabs1 = st.tabs(["🧤 Most Catches", "🧯 Most Stumpings", "🏃‍♂️ Most Run Outs", 
                     "🎳 Most Bowled"])

    with tabs1[0]:
        most_catches_df = pd.read_sql(queries.most_catches(), engine)
        st.markdown("### 🧤 Most Catches Leaderboard")
        st.table(style_table(most_catches_df))

    with tabs1[1]:
        stump = pd.read_sql(queries.most_stumpings(), engine)
        st.markdown("### 🧯 Top 10 Players with Most Stumpings")
        st.table(style_table(stump))

    with tabs1[2]:
        ro = pd.read_sql(queries.most_runouts(), engine)
        st.markdown("### 🏃‍♂️ Top 10 Players with Most Run Outs")
        st.table(style_table(ro))

    with tabs1[3]:
        bowled = pd.read_sql(queries.most_bowled(), engine)
        st.markdown("### 🎳 Top 10 Player taken Most Bowled Dismissals")
        st.table(style_table(bowled))

else:
    ############ EXTRAS ##########
    st.markdown("### 🏏 Extra Runs Analysis")
    tabs2 = st.tabs(["➕ Extras Breakdown", "🧢 Byes Analysis"])

    with tabs2[0]:
        extras_df = pd.read_sql(queries.extras(), engine)
        st.markdown("### ➕ Teams with Most Extras")
        st.table(style_table(extras_df))

    with tabs2[1]:
        byes = pd.read_sql(queries.byes(), engine)
        st.markdown("### 🧢 Byes Analysis")
        st.table(style_table(byes))