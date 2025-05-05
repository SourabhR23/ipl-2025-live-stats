import streamlit as st
import pandas as pd
from db_connection import get_engine
import queries
from style_config import add_team_logo

engine = get_engine()

# Data extratced from Database using Queries
points_df = pd.read_sql(queries.get_pts_table(), engine)

nrr_df = pd.read_sql(queries.nrr(), engine)

# Merge and calculate
merged = pd.merge(points_df, nrr_df, how='outer', left_on='Team', right_on='Team')
merged['Points'] = merged['Wins'] * 2 + merged['NR'] * 1

# Sort first by points (descending), then NRR (descending)
sorted_teams = merged.sort_values(by=['Points', 'NRR'], ascending=[False, False])

# Final table with ranked output
final_table = sorted_teams[['Team', 'Shortname', 'Matches', 'Wins', 'Loss', 'NR', 'Points', 'NRR']]


# Streamlit app
st.set_page_config(page_title="IPL Points Table", layout="wide")
st.title("🏏 IPL 2025 Points Table")

# Styling function
final_table['Teams'] = final_table.apply(lambda row: add_team_logo(row, col='Team'), axis=1)

# Rearranging columns
final_table_display = final_table[['Teams', 'Shortname', 'Matches', 'Wins', 'Loss', 'NR', 'Points', 'NRR']]

# Display
def create_html_table(df):
    html = "<table style='width:100%; border-collapse: collapse;'>"
    # Header
    html += "<tr>" + "".join(f"<th style='padding:8px;border-bottom:1px solid #444;color:white;text-align:left;'>{col}</th>" for col in df.columns) + "</tr>"
    # Rows
    for _, row in df.iterrows():
        html += "<tr>"
        for val in row:
            html += f"<td style='padding:8px;border-bottom:1px solid #333;color:white;'>{val}</td>"
        html += "</tr>"
    html += "</table>"
    return html

st.markdown("### 🏆 Ranked Teams")
st.markdown(create_html_table(final_table_display), unsafe_allow_html=True)
