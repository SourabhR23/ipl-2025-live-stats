def most_catches():
    return """
        SELECT 
            fielder_name AS Player,
            SUM(catches) AS `Total Catches`,
            MAX(catches) AS MAX
        FROM fielding_df
        GROUP BY fielder_name
        ORDER BY `Total Catches` DESC
        LIMIT 10;
    """ 

def most_stumpings():
    return """
        SELECT 
            fielder_name AS Player,
            SUM(stumpings) AS `Total Stumpings`,
            MAX(stumpings) AS MAX
        FROM fielding_df
        GROUP BY fielder_name
        ORDER BY `Total Stumpings` DESC
        LIMIT 10;
    """ 

def most_runouts():
    return """
        SELECT 
            fielder_name AS Player,
            SUM(runouts) AS `Total RunOuts`
        FROM fielding_df
        GROUP BY fielder_name
        ORDER BY `Total RunOuts` DESC
        LIMIT 10;
    """ 

def most_bowled():
    return """
        SELECT 
            fielder_name AS Player,
            SUM(bowled) AS `Total Bowled`,
            MAX(bowled) AS MAX
        FROM fielding_df
        GROUP BY fielder_name
        ORDER BY `Total Bowled` DESC
        LIMIT 10;
    """ 

def extras():
    return """
        SELECT 
            REPLACE(inning_name, ' Inning 1', '') AS TEAM,
            SUM(extra_runs) as EXTRAs
        FROM extras_df
        GROUP BY TEAM
        ORDER BY EXTRAs DESC;
    """ 

def byes():
    return """
        SELECT 
            REPLACE(inning_name, ' Inning 1', '') AS TEAM,
            SUM(byes) as `Byes Runs`
        FROM extras_df
        GROUP BY TEAM
        ORDER BY `Byes Runs` DESC;
    """ 


