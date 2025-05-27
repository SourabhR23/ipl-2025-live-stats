import pandas as pd
import squad_queries
from db_connection import get_engine

engine = get_engine()

def generate_fantasy_xi_for_match(team1, team2, recent_n, strategy="balanced", engine=None):

    squad_df = pd.read_sql(squad_queries.all_squad(), engine)
    batting_df = pd.read_sql(squad_queries.all_batting(), engine)
    bowling_df = pd.read_sql(squad_queries.all_bowling(), engine)

    selected_squad = squad_df[squad_df['teamName'].isin([team1, team2])].copy()
    player_ids = selected_squad['playerId'].astype(str).unique()

    # Filter recent matches
    # Fetch matches involving either team1 or team2
    matches_df = pd.read_sql("SELECT match_id, date, team1, team2 FROM matches ORDER BY date DESC", engine)
    team_matches = matches_df[
        (matches_df['team1'].isin([team1, team2])) | (matches_df['team2'].isin([team1, team2]))
    ]

    # Get last `recent_n` matches involving these two teams
    recent_match_ids = team_matches.sort_values('date', ascending=False).head(recent_n)['match_id'].tolist()

    # Now filter performance only from these matches
    bat_recent = batting_df[
        (batting_df['batsman_id'].astype(str).isin(player_ids)) &
        (batting_df['match_id'].isin(recent_match_ids))
    ]
    bowl_recent = bowling_df[
        (bowling_df['bowler_id'].astype(str).isin(player_ids)) &
        (bowling_df['match_id'].isin(recent_match_ids))
    ]

    # Aggregate performance
    bat_stats = bat_recent.groupby('batsman_id').agg({'runs': 'sum'}).rename(columns={'runs': 'Runs'})
    bowl_stats = bowl_recent.groupby('bowler_id').agg({'wickets': 'sum'}).rename(columns={'wickets': 'Wickets'})

    selected_squad['playerId'] = selected_squad['playerId'].astype(str)
    merged = selected_squad.set_index('playerId').join(bat_stats).join(bowl_stats).fillna(0).reset_index()
    merged['Impact Score'] = merged['Runs'] + (merged['Wickets'] * 20)
    merged['role'] = merged['role'].str.lower()

    # Strategy
    if strategy == "batting":
        bat_ct, bowl_ct, ar_ct = 5, 2, 2
    elif strategy == "bowling":
        bat_ct, bowl_ct, ar_ct = 2, 5, 2
    else:  # balanced
        bat_ct, bowl_ct, ar_ct = 4, 3, 3

    wk = merged[merged['role'].str.contains('wk')].nlargest(1, 'Impact Score')
    bat = merged[merged['role'].str.contains('batsman')].nlargest(bat_ct, 'Impact Score')
    ar = merged[merged['role'].str.contains('allrounder')].nlargest(ar_ct, 'Impact Score')
    bowl = merged[merged['role'].str.contains('bowler')].nlargest(bowl_ct, 'Impact Score')

    dream_xi = pd.concat([wk, bat, ar, bowl]).drop_duplicates(subset='playerName').nlargest(11, 'Impact Score')

    # Limit overseas players to 4
    while dream_xi[dream_xi['country'] != 'India'].shape[0] > 4:
        foreign = dream_xi[dream_xi['country'] != 'India']
        dream_xi = dream_xi.drop(foreign.nsmallest(1, 'Impact Score').index)
        # Replace with next-best Indian player
        replacement = merged[~merged['playerId'].isin(dream_xi['playerId']) & (merged['country'] == 'India')]
        if not replacement.empty:
            dream_xi = pd.concat([dream_xi, replacement.nlargest(1, 'Impact Score')])

    return dream_xi[['playerName', 'role', 'country', 'Runs', 'Wickets', 'Impact Score']]
