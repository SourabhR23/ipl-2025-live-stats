def get_batting_scorecard(match_id):
    return f"SELECT REPLACE(inning_name, ' Inning 1', '') as inning_name, batsman_name, runs, balls, fours, sixes, strike_rate, dismissal, dismissal_text, bowler_name, catcher_name FROM batting_df WHERE match_id = '{match_id}';"

def get_bowling_scorecard(match_id):
    return f"SELECT REPLACE(inning_name, ' Inning 1', '') as inning_name, bowler_name, overs, maidens, runs_conceded, wickets, no_balls, wides, economy FROM bowling_df WHERE match_id = '{match_id}';"
