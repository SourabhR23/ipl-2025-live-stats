def most_wickets():
    return """
        WITH bowler_base AS (
            SELECT 
                b.bowler_name,
                s.teamName AS Team,
                b.match_id,
                CAST(b.overs AS DECIMAL(4,1)) AS overs,
                b.wickets,
                b.runs_conceded
            FROM bowling_df b
            JOIN squad_df s ON b.bowler_id = s.playerId
        ),

        bowler_stats AS (
            SELECT 
                bowler_name,
                Team,
                COUNT(DISTINCT match_id) AS Matches,
                SUM(overs) AS Overs,
                SUM(FLOOR(overs) * 6 + ROUND((overs - FLOOR(overs)) * 10)) AS Balls,
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
                    (SUM(FLOOR(overs) * 6 + ROUND((overs - FLOOR(overs)) * 10)) / 6), 
                    2
                ) AS Economy,

                ROUND(
                    CASE 
                        WHEN SUM(wickets) > 0 THEN 
                            SUM(FLOOR(overs) * 6 + ROUND((overs - FLOOR(overs)) * 10)) / SUM(wickets)
                        ELSE NULL
                    END, 2
                ) AS `Strike Rate`
            FROM bowler_base
            GROUP BY bowler_name, Team
        ),

        bbi_per_bowler AS (
            SELECT 
                b.bowler_name,
                CONCAT(MIN(b.runs_conceded), '/', b.wickets) AS BBI
            FROM bowling_df b
            WHERE (b.bowler_name, b.wickets) IN (
                SELECT 
                    bowler_name, MAX(wickets)
                FROM bowling_df
                GROUP BY bowler_name
            )
            GROUP BY b.bowler_name, b.wickets
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
        ORDER BY s.Wickets DESC
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

def total_wkts():
    return"""
        SELECT SUM(wickets) as `Total Wickets`
        FROM innings;
        """