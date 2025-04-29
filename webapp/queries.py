def get_all_matches():
    return "SELECT * FROM IPL_Match_List ORDER BY date;"

def get_batting_scorecard(match_id):
    return f"SELECT * FROM batting_scorecard WHERE match_id = '{match_id}';"

def get_bowling_scorecard(match_id):
    return f"SELECT * FROM bowling_scorecard WHERE match_id = '{match_id}';"
