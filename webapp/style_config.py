import pandas as pd
import streamlit as st

def scorecard(team, runs, wickets, overs, color):
    return f"""
    <div style="background-color:{color}; padding:20px; border-radius:15px; text-align:center;">
        <h3 style="color:white;">{team}</h3>
        <h2 style="color:white;">{runs} / {wickets}</h2>
        <p style="color:white;">Overs: {overs}</p>
    </div>
    """

def styled_table(df, highlight_col=None, name_col=None):
    style = df.style.set_properties(**{
        'background-color': '#1e1e1e',
        'color': 'white',
        'text-align': 'center',
        'font-size': '14px',
        'border': '1px solid #333'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('background-color', '#111'), ('color', 'white'), ('text-align', 'center')]
    }]).format({col: '{:,.0f}' for col in df.select_dtypes(include='number').columns})
    
    # Highlight highest runs in columns
    if highlight_col in df.columns:
        style = style.highlight_max(subset=[highlight_col], color='#2ecc71', axis=0)
    
    # Highlight name of player with highest runs
    if name_col and highlight_col and highlight_col in df.columns and name_col in df.columns:
        max_val = df[highlight_col].max()
        style = style.apply(lambda row: [
            'color: #f39c12; font-weight: bold;' if row[highlight_col] == max_val and col == name_col else ''
            for col in df.columns
        ], axis=1)

    return style

def render_innings(innings_name, bat_df, bowl_df, opponent_name):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### 🏏 Batting - {innings_name}")
        styled_bat_df = styled_table(bat_df.iloc[:, 1:], 
                                     highlight_col='runs',
                                     name_col='batsman_name' if 'batsman_name' in bat_df.columns else None)
        st.dataframe(styled_bat_df, use_container_width=True, hide_index=True)


    with col2:
        st.markdown(f"### 🎯 Bowling - {opponent_name}")
        styled_bowl_df = styled_table(bowl_df.iloc[:, 1:], 
                                      highlight_col='wickets',
                                      name_col='bowler_name' if 'bowler_name' in bowl_df.columns else None)
        st.dataframe(styled_bowl_df, use_container_width=True, hide_index=True)
        
TEAM_COLORS = {
    "Kolkata Knight Riders": "#301934",       # Purple
    "Mumbai Indians": "#2980b9",              # Blue
    "Chennai Super Kings": "#f1c40f",         # Yellow
    "Royal Challengers Bengaluru": "#c0392b", # Red
    "Delhi Capitals": "#6495ED",              # Lighter Blue
    "Rajasthan Royals": "#C70593",            # Pink
    "Gujarat Titans": "#1B2133",              # Teal
    "Sunrisers Hyderabad": "#F85E12",         # Orange
    "Lucknow Super Giants": "#002066",        # Navy Blue
    "Punjab Kings": "#590016"                 # Crimson       
}

def get_team_color(team):
    return TEAM_COLORS.get(team, "#555")  # fallback gray
        
def style_table(df: pd.DataFrame):
    return (
        df.style
        .set_properties(**{
            'background-color': '#121212',   # deep dark gray
            'color': 'white',
            'border-color': '#333',
            'font-size': '12px',
            'text-align': 'center'
        })
        .set_table_styles([{
            'selector': 'th',
            'props': [('background-color', '#1f1f1f'),
                      ('color', 'white'),
                      ('font-weight', 'bold'),
                      ('text-align', 'center')]
        }])
        .format(na_rep="-", formatter={col: '{:,.0f}' for col in df.select_dtypes(include=['float', 'int']).columns})
    )

def ballstyle_table(df: pd.DataFrame):
    return (
        df.style
        .set_properties(**{
            'background-color': '#121212',   # deep dark gray
            'color': 'white',
            'border-color': '#333',
            'font-size': '12px',
            'text-align': 'center'
        })
        .set_table_styles([{
            'selector': 'th',
            'props': [('background-color', '#1f1f1f'),
                      ('color', 'white'),
                      ('font-weight', 'bold'),
                      ('text-align', 'center')]
        }]).format(na_rep="-", formatter={
            col: '{:,.1f}' if col == 'Overs' else '{:,.0f}'
            for col in df.select_dtypes(include=['float', 'int']).columns
        })
    )

def render_cap_holder(cap_type, name, value, color, emoji, unit):
    st.sidebar.markdown(f"""
    <div style='background-color:{color};padding:16px;border-radius:12px;text-align:center;margin-bottom:10px;box-shadow: 0 4px 10px rgba(0,0,0,0.3);'>
        <div style='font-size:20px;'>{emoji} <b>{cap_type} Cap</b></div>
        <div style='font-size:18px;font-weight:bold;color:white;margin-top:10px;'>{name}</div>
        <div style='font-size:14px;color:white;'>✨ <b>{value} {unit}</b></div>
    </div>
    """, unsafe_allow_html=True)