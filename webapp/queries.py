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
            p.batsman_name AS Batsman,
            p.runs AS 'Highest Runs',
            p.opponent_team AS 'Opponent Team'
        FROM player_performance p
        JOIN max_scores m
            ON p.batsman_name = m.batsman_name AND p.runs = m.highest_runs
        ORDER BY p.runs DESC 
        LIMIT 10;
    """

def strike_rate():
    return """
        SELECT 
            b.batsman_name AS Batsman,
            SUM(b.runs) AS 'Total Runs',
            COUNT(b.match_id) AS 'Matches',
            COUNT(b.inning_name) AS 'Innings',
            ROUND(SUM(b.runs) / NULLIF(COUNT(b.dismissal), 0), 2) AS Average,
            ROUND(SUM(b.runs) * 100.0 / NULLIF(SUM(b.balls), 0), 2) AS StrikeRate
        FROM batting_df b
        JOIN squad_df s
            ON b.batsman_name = s.playerName
        WHERE s.role LIKE '%%Bat%%'
        GROUP BY b.batsman_name
        ORDER BY StrikeRate DESC
        LIMIT 10;
    """

def get_century_stats():
    return """
        SELECT 
            batsman_name as Batsman, 
            COUNT(*) AS Innings,
            SUM(runs) AS `Total Runs`,
            COUNT(CASE WHEN runs >= 100 THEN 1 END) AS `100s`,
            MAX(runs) AS 'Highest Score'
        FROM batting_df
        GROUP BY batsman_name
        HAVING `100s` > 0
        ORDER BY `Total Runs` DESC
        LIMIT 10;
    """

def get_half_century_stats():
    return """
        SELECT 
            batsman_name AS Batsman, 
            COUNT(*) AS Innings,
            SUM(runs) AS `Total Runs`,
            COUNT(CASE WHEN runs >= 50 THEN 1 END) AS `50s`,
            MAX(runs) AS `Highest Score`
        FROM batting_df
        GROUP BY batsman_name
        HAVING `50s` > 0
        ORDER BY `50s` DESC, `Highest Score` DESC
        LIMIT 10;
    """

def get_ninties():
    return """
        SELECT 
            batsman_name as Batsman, 
            COUNT(*) AS Innings,
            SUM(runs) AS `Total Runs`,
            COUNT(CASE WHEN runs >= 90 AND runs < 100 THEN 1 END) AS `90s`,
            MAX(runs) AS 'Highest Score'
        FROM batting_df
        GROUP BY batsman_name
        HAVING `90s` > 0
        ORDER BY `Total Runs` DESC
        LIMIT 10;
    """

def get_sixes():
    return """
        SELECT 
            batsman_name AS Batsman,
            COUNT(*) AS Innings, 
            SUM(runs) AS `Total Runs`, 
            SUM(sixes) AS `6s`
        FROM batting_df
        GROUP BY batsman_name
        ORDER BY `6s` DESC, `Total Runs` DESC
        LIMIT 10;
    """

def get_fours():
    return """
        SELECT 
            batsman_name AS Batsman,
            COUNT(*) AS Innings, 
            SUM(runs) AS `Total Runs`, 
            SUM(fours) AS `4s`
        FROM batting_df
        GROUP BY batsman_name
        ORDER BY `4s` DESC, `Total Runs` DESC
        LIMIT 10;
    """

