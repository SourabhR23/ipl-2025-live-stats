import pandas as pd
import streamlit as st
import base64
import os

# ─────────────────────────────────────────────
# 🔧 Constants
# ─────────────────────────────────────────────
IPL_LOGO_PATH = os.path.join("webapp", "images", "Tata_IPL.png")

TEAM_COLORS = {
    "Kolkata Knight Riders": "#301934",
    "Mumbai Indians": "#2980b9",
    "Chennai Super Kings": "#f1c40f",
    "Royal Challengers Bengaluru": "#c0392b",
    "Delhi Capitals": "#6495ED",
    "Rajasthan Royals": "#C70593",
    "Gujarat Titans": "#1B2133",
    "Sunrisers Hyderabad": "#F85E12",
    "Lucknow Super Giants": "#002066",
    "Punjab Kings": "#590016"
}

TEAM_LOGO_PATHS = {
    "Kolkata Knight Riders": os.path.join("webapp", "images", "Kolkata.png"),
    "Mumbai Indians": os.path.join("webapp", "images", "Mumbai.png"),
    "Chennai Super Kings": os.path.join("webapp", "images", "Chennai.png"),
    "Royal Challengers Bengaluru": os.path.join("webapp", "images", "Bengaluru.png"),
    "Delhi Capitals": os.path.join("webapp", "images", "Delhi.png"),
    "Rajasthan Royals": os.path.join("webapp", "images", "Rajasthan.png"),
    "Gujarat Titans": os.path.join("webapp", "images", "Gujarat.png"),
    "Sunrisers Hyderabad": os.path.join("webapp", "images", "Hyderabad.png"),
    "Lucknow Super Giants": os.path.join("webapp", "images", "Lucknow.png"),
    "Punjab Kings": os.path.join("webapp", "images", "Punjab.png")
}

# ─────────────────────────────────────────────
# 🎨 Layout and Branding
# ─────────────────────────────────────────────

def render_logo_and_title(title):
    logo_html = ""
    if os.path.exists(IPL_LOGO_PATH):
        with open(IPL_LOGO_PATH, "rb") as f:
            encoded_logo = base64.b64encode(f.read()).decode()
        logo_html = f"<img src='data:image/png;base64,{encoded_logo}' width='160' style='vertical-align:middle; margin-right:10px;'>"
    
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:16px; margin-bottom: 10px;'>
        {logo_html}
        <h1 style='color:#f5f5f5; margin:0;'>{title}</h1>
    </div>
    """, unsafe_allow_html=True)

def render_team_grid():
    cols = st.columns(5)
    for i, (team, logo_path) in enumerate(TEAM_LOGO_PATHS.items()):
        with cols[i % 5]:
            color = TEAM_COLORS.get(team, "#444")
            logo_html = "⚠️"
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as img:
                    encoded = base64.b64encode(img.read()).decode()
                    logo_html = f'<img src="data:image/png;base64,{encoded}" width="90">'
            st.markdown(f"""
                <div style="background-color:{color};padding:12px;border-radius:12px;
                            text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.4);
                            min-height:150px;display:flex;flex-direction:column;justify-content:center;">
                    <div style="height: 70px; display: flex; align-items: center; justify-content: center;">{logo_html}</div>
                    <p style="margin-top:8px;color:white;font-size:15px;"><b>{team}</b></p>
                </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 🏏 Visual Components
# ─────────────────────────────────────────────

def get_team_logo_path(team_name):
    for name, path in TEAM_LOGO_PATHS.items():
        if name in team_name:
            return path
    return None

def get_team_color(team):
    return TEAM_COLORS.get(team, "#555")

def scorecard(team, runs, wickets, overs, color, logo_path=None):
    logo_html = ""
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
            logo_html = f"<img src='data:image/png;base64,{encoded}' width='160' style='margin-left:10px;'>"

    return f"""
    <div style="background-color:{color}; padding:20px; border-radius:15px;
                display:flex; justify-content:space-between; align-items:left;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
        <div>{logo_html}</div>
        <div style="text-align:right; flex:1;">
            <h2 style="color:white; margin:0;">{team}</h2>
            <h1 style="color:white; margin:5px 0; font-size:36px;">{runs} / {wickets}</h1>
            <p style="color:white; margin:0; font-size:18px;">Overs: {overs}</p>
        </div>
    </div>
    """

def render_cap_holder(cap_type, name, team, value, color, emoji, unit):
    st.sidebar.markdown(f"""
    <div style='background-color:{color};padding:16px;border-radius:12px;
                text-align:center;margin-bottom:10px;box-shadow: 0 4px 10px rgba(0,0,0,0.3);'>
        <div style='font-size:20px;'>{emoji} <b>{cap_type} Cap</b></div>
        <div style='font-size:18px;font-weight:bold;color:white;margin-top:10px;'>{name}</div>
        <div style='font-size:12px;font-weight:bold;color:white;margin-top:10px;'>{team}</div>
        <div style='font-size:14px;color:white;'>✨ <b>{value} {unit}</b></div>
    </div>
    """, unsafe_allow_html=True)

def add_team_logo(row, col='Team'):
    team_name = row[col]
    logo_path = TEAM_LOGO_PATHS.get(team_name, '')
    if logo_path and os.path.exists(logo_path):
        with open(logo_path, 'rb') as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        return f"""<img src='data:image/png;base64,{encoded}' width='24'> {team_name}"""
    return team_name

# ─────────────────────────────────────────────
# 📊 Table Styling
# ─────────────────────────────────────────────

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

def style_table(df: pd.DataFrame):
    return (
        df.style
        .set_properties(**{
            'background-color': '#121212',
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
        .format(na_rep="-", formatter={
            col: '{:,.2f}' if col in ['Economy', 'Avg', 'SR'] else ('{:,.1f}' if col == 'Overs' else '{:,.0f}')
            for col in df.select_dtypes(include=['float', 'int']).columns
        })
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

# ─────────────────────────────────────────────
# 🔁 Render Innings Block
# ─────────────────────────────────────────────

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
