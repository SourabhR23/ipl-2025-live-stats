def most_runs():
    return """
        SELECT 
            batsman_name AS Batsman,
            REPLACE(inning_name, ' Inning 1', '') AS Team,
            COUNT(DISTINCT match_id) AS Matches,
            SUM(CASE WHEN dismissal IS NULL THEN 1 ELSE 0 END) AS NotOuts,
            MAX(runs) AS HighScore,
            SUM(runs) AS Runs,
            ROUND(SUM(runs) * 1.0 / NULLIF(COUNT(*) - SUM(CASE WHEN dismissal IS NULL THEN 1 ELSE 0 END), 0), 2) AS Avg,
            SUM(balls) AS `Balls Faced`,
            ROUND(SUM(runs) * 100.0 / NULLIF(SUM(balls), 0), 2) AS SR,
            SUM(CASE WHEN runs >= 100 THEN 1 ELSE 0 END) AS `100`,
            SUM(CASE WHEN runs >= 50 AND runs < 100 THEN 1 ELSE 0 END) AS `50`,
            SUM(fours) AS `4s`,
            SUM(sixes) AS `6s`
        FROM batting_df
        GROUP BY batsman_id, batsman_name, Team
        ORDER BY Runs DESC
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
            SELECT 
                a.batsman_name, 
                a.runs,
                a.inning_name,
                REPLACE(b.inning_name, ' Inning 1', '') AS opponent_team
            FROM batting_df a
            JOIN batting_df b 
                ON a.match_id = b.match_id 
                AND a.inning_name != b.inning_name
        )
        SELECT DISTINCT 
            p.batsman_name AS Batsman,
            REPLACE(p.inning_name, ' Inning 1', '') AS Team,
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
            REPLACE(inning_name, ' Inning 1', '') AS Team, 
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
            REPLACE(inning_name, ' Inning 1', '') AS Team, 
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
            REPLACE(inning_name, ' Inning 1', '') AS Team, 
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
            REPLACE(inning_name, ' Inning 1', '') AS Team,
            SUM(sixes) AS `6s`,
            COUNT(*) AS Innings, 
            SUM(runs) AS `Total Runs`
        FROM batting_df
        GROUP BY batsman_name
        ORDER BY `6s` DESC, `Total Runs` DESC
        LIMIT 10;
    """

def get_fours():
    return """
        SELECT 
            batsman_name AS Batsman,
            REPLACE(inning_name, ' Inning 1', '') AS Team,
            SUM(fours) AS `4s`,
            COUNT(*) AS Innings, 
            SUM(runs) AS `Total Runs`
        FROM batting_df
        GROUP BY batsman_name
        ORDER BY `4s` DESC, `Total Runs` DESC
        LIMIT 10;
    """

def total_runs():
    return"""
        SELECT SUM(runs) as Runs
        FROM innings;
        """