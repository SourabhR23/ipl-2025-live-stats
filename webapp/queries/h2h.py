# Innings table
def inn():
    return """
        SELECT 
            match_id, 
            REPLACE(inning_name, ' Inning 1', '') AS team, 
            runs 
        FROM innings    
    """


# Top Batting Performers
def top_batsmen_query(h2h_ids):
    return f"""
        SELECT 
            batsman_name AS Player, 
            REPLACE(inning_name, ' Inning 1', '') AS Team,
            SUM(runs) AS Runs
        FROM batting_df
        WHERE match_id IN {h2h_ids}
        GROUP BY batsman_name
        ORDER BY Runs DESC
        LIMIT 5;
    """

# Top Bowling Performers
def top_bowlers_query(h2h_ids):
    return f"""
        SELECT 
            bowler_name AS Player, 
            REPLACE(inning_name, ' Inning 1', '') AS Against,
            SUM(wickets) AS Wickets
        FROM bowling_df
        WHERE match_id IN {h2h_ids}
        GROUP BY bowler_name
        ORDER BY Wickets DESC
        LIMIT 5;
    """