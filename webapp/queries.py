def get_all_matches():
    """
    Returns an SQL query string to retrieve details of all matches from the 'matches' table.
    """
    return ("SELECT match_id, match_name, status, venue, date, match_winner FROM matches;")

def get_batting_scorecard(match_id):
    """
    Returns an SQL query string to retrieve the batting scorecard for a specific match. It takes the 'match_id' as input.
    """
    return f"SELECT REPLACE(inning_name, ' Inning 1', '') as inning_name, batsman_name, runs, balls, fours, sixes, strike_rate, dismissal, dismissal_text, bowler_name, catcher_name FROM batting_df WHERE match_id = '{match_id}';"

def get_bowling_scorecard(match_id):
    """
    Returns an SQL query string to retrieve the bowling scorecard for a specific match. It takes the 'match_id' as input.
    """
    return f"SELECT REPLACE(inning_name, ' Inning 1', '') as inning_name, bowler_name, overs, maidens, runs_conceded, wickets, no_balls, wides, economy FROM bowling_df WHERE match_id = '{match_id}';"

def get_innings_details(march_id):
    return f"SELECT REPLACE(inning_name, ' Inning 1', '') as inning_name, runs, wickets, overs FROM innings WHERE match_id = '{march_id}';"

def most_runs():
    return """
        SELECT 
            batsman_name,
            REPLACE(inning_name, ' Inning 1', '') AS Team,
            SUM(runs) AS RUNS,
            SUM(fours) AS FOURS,
            SUM(sixes) AS SIXES,
            COUNT(match_id) AS MATCHES
        FROM batting_df
        GROUP BY inning_name, batsman_name
        ORDER BY RUNS DESC
        LIMIT 10;
    """

def high_scores():
    return """
        WITH max_scores AS (
            SELECT batsman_name, MAX(runs) AS highest_runs
            FROM batting_df
            GROUP BY batsman_name
        ),
        player_performance AS (
            SELECT a.batsman_name, a.runs,
            REPLACE(b.inning_name, ' Inning 1', '') AS opponent_team
            FROM batting_df a
            JOIN batting_df b 
                ON a.match_id = b.match_id 
                AND a.inning_name != b.inning_name
        )
        SELECT DISTINCT 
            p.batsman_name,
            p.runs AS highest_runs,
            p.opponent_team
        FROM player_performance p
        JOIN max_scores m
            ON p.batsman_name = m.batsman_name AND p.runs = m.highest_runs
        ORDER BY p.runs DESC;
    """

def get_century_stats():
    return """
        SELECT 
            batsman_name,
            COUNT(*) AS centuries,
            SUM(runs) AS total_runs_in_100_plus
        FROM batting_df
        WHERE runs >= 100
        GROUP BY batsman_name
        ORDER BY runs DESC;
    """


