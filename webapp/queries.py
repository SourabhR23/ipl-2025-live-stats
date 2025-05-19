def get_live_match():
    return"""
        select * from IPL_Match_List;
    """

def get_all_matches():
    return """
        SELECT 
                match_id, 
                match_name, 
                status, 
                venue, 
                date,
                toss_winner,
                toss_choice, 
                match_winner,
                team1,
                team2
        FROM matches;"""

def get_batting_scorecard(match_id):
    return f"SELECT REPLACE(inning_name, ' Inning 1', '') as inning_name, batsman_name, runs, balls, fours, sixes, strike_rate, dismissal, dismissal_text, bowler_name, catcher_name FROM batting_df WHERE match_id = '{match_id}';"

def get_bowling_scorecard(match_id):
    return f"SELECT REPLACE(inning_name, ' Inning 1', '') as inning_name, bowler_name, overs, maidens, runs_conceded, wickets, no_balls, wides, economy FROM bowling_df WHERE match_id = '{match_id}';"

def get_innings_details(march_id):
    return f"SELECT REPLACE(inning_name, ' Inning 1', '') as inning_name, runs, wickets, overs FROM innings WHERE match_id = '{march_id}';"

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

def most_wickets():
    return """
            WITH bowler_stats AS (
                SELECT 
                    bowler_name,
                    REPLACE(b.inning_name, ' Inning 1', '') AS Team,
                    COUNT(DISTINCT match_id) AS Matches,
                    SUM(CAST(overs AS DECIMAL(4,1))) AS Overs,
                    SUM(FLOOR(CAST(overs AS DECIMAL(4,1))) * 6 + ROUND((CAST(overs AS DECIMAL(4,1)) - FLOOR(CAST(overs AS DECIMAL(4,1)))) * 10)) AS Balls,
                    SUM(wickets) AS Wickets,
                    SUM(runs_conceded) AS `Runs Conceded`,
                    SUM(CASE WHEN wickets = 4 THEN 1 ELSE 0 END) AS `4W`,
                    SUM(CASE WHEN wickets >= 5 THEN 1 ELSE 0 END) AS `5W`,

                    ROUND(
                        CASE 
                            WHEN SUM(wickets) > 0 THEN SUM(runs_conceded) / SUM(wickets)
                            ELSE NULL
                        END, 2
                    ) AS Average,

                    ROUND(
                        SUM(runs_conceded) / 
                        (SUM(FLOOR(CAST(overs AS DECIMAL(4,1))) * 6 + ROUND((CAST(overs AS DECIMAL(4,1)) - FLOOR(CAST(overs AS DECIMAL(4,1)))) * 10)) / 6), 
                        2
                    ) AS Economy,

                    ROUND(
                        CASE 
                            WHEN SUM(wickets) > 0 THEN 
                                SUM(FLOOR(CAST(overs AS DECIMAL(4,1))) * 6 + ROUND((CAST(overs AS DECIMAL(4,1)) - FLOOR(CAST(overs AS DECIMAL(4,1)))) * 10)) / SUM(wickets)
                            ELSE NULL
                        END, 2
                    ) AS `Strike Rate`
                FROM bowling_df
                GROUP BY bowler_name
            ),

            bbi_per_bowler AS (
                SELECT 
                    bowler_name,
                    CONCAT(MIN(runs_conceded), '/', wickets) AS BBI
                FROM bowling_df
                WHERE (bowler_name, wickets) IN (
                    SELECT 
                        bowler_name, MAX(wickets)
                    FROM bowling_df
                    GROUP BY bowler_name
                )
                GROUP BY bowler_name, wickets
            )

            SELECT 
                s.bowler_name AS Bowler,
                s.Team,
                s.Matches,
                s.Wickets,
                s.`Runs Conceded`,
                s.Overs,
                s.Balls,
                s.Average,
                s.Economy,
                s.`Strike Rate`,
                s.`4W`,
                s.`5W`,
                b.BBI

            FROM bowler_stats s
            LEFT JOIN bbi_per_bowler b ON s.bowler_name = b.bowler_name
            ORDER BY Wickets DESC
            LIMIT 10;
        """

def bowl_avg():
    return """
        SELECT 
            b.bowler_name AS Bowler,
            COUNT(DISTINCT b.match_id) AS Matches,
            SUM(CAST(b.overs AS DECIMAL(4,1))) AS Overs,
            SUM(b.wickets) AS Wickets,
            ROUND(SUM(b.runs_conceded) / SUM(b.wickets), 2) AS Avg

        FROM bowling_df b
        JOIN squad_df p ON b.bowler_id = p.playerId

        -- Include only bowlers and bowling allrounders
        WHERE p.role IN ('Bowler', 'Bowling Allrounder')

        GROUP BY b.bowler_name

        -- Include only bowlers with at least 1 wicket and more than 1 match
        HAVING Wickets > 0 AND Matches > 1

        ORDER BY Avg ASC
        LIMIT 10;
    """

def best_bowl():
    return """
        WITH ranked_performances AS (
            SELECT 
                bowler_name AS Bowler,
                TRIM(REPLACE(inning_name, SUBSTRING_INDEX(inning_name, 'Inning', -1), '')) AS Vs,
                overs AS Overs,
                runs_conceded AS Runs,
                wickets AS Wkts,
                CONCAT(wickets, '-', runs_conceded) AS Bbi,
                IF(maidens = 0, '-', maidens) AS Maidens,
                economy AS Economy,
                ROW_NUMBER() OVER (
                    PARTITION BY bowler_name
                    ORDER BY wickets DESC, runs_conceded ASC
                ) AS rn
            FROM bowling_df
        )

        SELECT 
            Bowler,
            Vs,
            Overs,
            Runs,
            Wkts,
            Bbi,
            Maidens,
            Economy
        FROM ranked_performances
        WHERE rn = 1
        ORDER BY Wkts DESC, Runs ASC
        LIMIT 10;
    """

def five_wkts():
    return """
        SELECT 
            bowler_name AS Bowler,
            REPLACE(inning_name, ' Inning 1', '') AS Against,
            overs AS Overs,
            maidens AS Maidens,
            runs_conceded AS Runs,
            wickets AS Wickets,
            CONCAT(wickets, '-', runs_conceded) AS BBI,
            economy AS Economy
        FROM bowling_df
        WHERE wickets >= 5
        ORDER BY wickets DESC, runs_conceded ASC;
    """

def best_eco():
    return """
        SELECT 
            bowler_name AS Bowler,
            COUNT(DISTINCT match_id) AS Matches,
            ROUND(SUM(CAST(overs AS DECIMAL(4,1))), 1) AS Overs,
            COUNT(*) AS Inns,
            SUM(wickets) AS Wkts,

            -- Total Balls from overs like 4.5 → 4*6 + 5 = 29
            ROUND(SUM(runs_conceded) / (SUM(FLOOR(CAST(overs AS DECIMAL(4,1))) * 6 + 
                    ROUND((CAST(overs AS DECIMAL(4,1)) - FLOOR(CAST(overs AS DECIMAL(4,1)))) * 10)) / 6), 2) AS Eco,

            ROUND(CASE 
                WHEN SUM(wickets) > 0 THEN SUM(runs_conceded) / SUM(wickets)
                ELSE NULL
            END, 2) AS Avg,

            ROUND(CASE 
                WHEN SUM(wickets) > 0 THEN 
                    (SUM(FLOOR(CAST(overs AS DECIMAL(4,1))) * 6 + 
                        ROUND((CAST(overs AS DECIMAL(4,1)) - FLOOR(CAST(overs AS DECIMAL(4,1)))) * 10))
                    ) / SUM(wickets)
                ELSE NULL
            END, 2) AS Sr

        FROM bowling_df
        GROUP BY bowler_name
        HAVING SUM(wickets) > 0
        ORDER BY Eco ASC
        LIMIT 10;
    """

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
