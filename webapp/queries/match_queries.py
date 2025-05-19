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

def get_innings_details(march_id):
    return f"SELECT REPLACE(inning_name, ' Inning 1', '') as inning_name, runs, wickets, overs FROM innings WHERE match_id = '{march_id}';"
