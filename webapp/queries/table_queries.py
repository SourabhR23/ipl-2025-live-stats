def get_pts_table():
    return """SELECT 
                teamname as Team,
                shortname as Shortname,
                matches as Matches,
                wins as Wins,
                loss as Loss,
                ties as Ties,
                nr as NR     
       FROM points_table; """

def nrr():
    return """
        WITH innings_balls AS (
        SELECT
            match_id,
            SUBSTRING_INDEX(inning_name, ' Inning', 1) AS Team,
            runs,
            FLOOR(overs) * 6 + ROUND((overs - FLOOR(overs)) * 10) AS balls
        FROM innings
        ),
        team_runs AS (
        SELECT
            team,
            SUM(runs) AS runs_scored,
            SUM(balls) AS balls_faced
        FROM innings_balls
        GROUP BY team
        ),
        opponent_runs AS (
        SELECT
            ib2.Team,
            SUM(ib1.runs) AS runs_conceded,
            SUM(ib1.balls) AS balls_bowled
        FROM innings_balls ib1
        JOIN innings_balls ib2
            ON ib1.match_id = ib2.match_id AND ib1.Team != ib2.Team
        GROUP BY ib2.team
        )
        SELECT
        t.Team,
        ROUND((t.runs_scored / t.balls_faced - o.runs_conceded / o.balls_bowled) * 6, 3) AS NRR
        FROM team_runs t
        JOIN opponent_runs o ON t.Team = o.Team
        ORDER BY NRR DESC;
    """