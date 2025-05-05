import os
import pandas as pd
import requests
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from config import API_KEY, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE

# Constants
BASE_URL = "https://api.cricapi.com/v1/match_scorecard"
POINTS_URL = "https://api.cricapi.com/v1/series_points"
MATCH_LIST_CSV = r"data/IPL_2025_Match_List.csv"
FETCH_LIMIT = 10

# Setup database connection
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}")

# Helper Functions
def fetch_match_data(match_id):
    params = {"apikey": API_KEY, "id": match_id}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        match_info = response.json()
        if match_info.get("status") == "success":
            return match_info.get("data", {})
    except Exception as e:
        print(f"❌ Error fetching match {match_id}: {e}")
    return None

def parse_match_data(match):
    matches_data, innings_data, batting_data, bowling_data, fielding_data, extras_data = [], [], [], [], [], []

    match_id = match.get('id')
    series_id = match.get('series_id')
    name = match.get('name')
    match_type = match.get('matchType')
    status = match.get('status')
    venue = match.get('venue')
    date = match.get('date')
    teams = match.get('teams', [])
    team1 = teams[0] if len(teams) > 0 else None
    team2 = teams[1] if len(teams) > 1 else None
    toss_winner = match.get('tossWinner')
    toss_choice = match.get('tossChoice')
    match_winner = match.get('matchWinner')

    # Match metadata
    matches_data.append({
        'match_id': match_id,
        'series_id': series_id,
        'match_name': name,
        'match_type': match_type,
        'status': status,
        'venue': venue,
        'date': date,
        'team1': team1,
        'team2': team2,
        'toss_winner': toss_winner,
        'toss_choice': toss_choice,
        'match_winner': match_winner
    })

    # Innings score (summary)
    for score in match.get('score', []):
        innings_data.append({
            'match_id': match_id,
            'inning_name': score.get('inning'),
            'runs': score.get('r'),
            'wickets': score.get('w'),
            'overs': score.get('o')
        })

    # Full detailed scorecard
    for innings in match.get('scorecard', []):
        inning_name = innings.get('inning')

        for batter in innings.get('batting', []):
            batsman = batter.get('batsman', {})
            bowler = batter.get('bowler', {})
            catcher = batter.get('catcher', {})
            batting_data.append({
                'match_id': match_id,
                'inning_name': inning_name,
                'batsman_id': batsman.get('id'),
                'batsman_name': batsman.get('name'),
                'runs': batter.get('r'),
                'balls': batter.get('b'),
                'fours': batter.get('4s'),
                'sixes': batter.get('6s'),
                'strike_rate': batter.get('sr'),
                'dismissal': batter.get('dismissal'),
                'dismissal_text': batter.get('dismissal-text'),
                'bowler_id': bowler.get('id'),
                'bowler_name': bowler.get('name'),
                'catcher_id': catcher.get('id'),
                'catcher_name': catcher.get('name')
            })

        for bowler in innings.get('bowling', []):
            bowler_info = bowler.get('bowler', {})
            bowling_data.append({
                'match_id': match_id,
                'inning_name': inning_name,
                'bowler_id': bowler_info.get('id'),
                'bowler_name': bowler_info.get('name'),
                'overs': bowler.get('o'),
                'maidens': bowler.get('m'),
                'runs_conceded': bowler.get('r'),
                'wickets': bowler.get('w'),
                'no_balls': bowler.get('nb'),
                'wides': bowler.get('wd'),
                'economy': bowler.get('eco')
            })

        for fielder in innings.get('catching', []):
            catcher_info = fielder.get('catcher', {})
            fielding_data.append({
                'match_id': match_id,
                'inning_name': inning_name,
                'fielder_id': catcher_info.get('id'),
                'fielder_name': catcher_info.get('name'),
                'catches': fielder.get('catch'),
                'stumpings': fielder.get('stumped'),
                'runouts': fielder.get('runout'),
                'bowled': fielder.get('bowled')
            })

        extras = innings.get('extras', {})
        extras_data.append({
            'match_id': match_id,
            'inning_name': inning_name,
            'extra_runs': extras.get('r', 0),
            'byes': extras.get('b', 0)
        })

    return matches_data, innings_data, batting_data, bowling_data, fielding_data, extras_data

def fetch_points_table(match_id):
    pts_data = []
    params = {"apikey": API_KEY, "id": match_id}
    try:
        response = requests.get(POINTS_URL, params=params, timeout=10)
        response.raise_for_status()
        points_json = response.json()
        if points_json.get("status") == "success":
            for team in points_json.get("data", []):
                pts_data.append({
                    'teamname': team.get('teamname'),
                    'shortname': team.get('shortname'),
                    'matches': team.get('matches'),
                    'wins': team.get('wins'),
                    'loss': team.get('loss'),
                    'ties': team.get('ties'),
                    'nr': team.get('nr')
                })
    except Exception as e:
        print(f"❌ Error fetching points table: {e}")
    return pts_data
# Main Execution
def main():
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"🏏 Fetching matches for {yesterday}")

    match_list = pd.read_csv(MATCH_LIST_CSV)
    match_list['match_date'] = pd.to_datetime(match_list['match_date']).dt.date
    yesterday_matches = match_list[match_list['match_date'] == datetime.strptime(yesterday, '%Y-%m-%d').date()]

    if yesterday_matches.empty:
        print("🎉 No matches played yesterday.")
        return

    pending_ids = yesterday_matches['id'].tolist()
    print(f"📝 {len(pending_ids)} matches to fetch.")

    all_matches, all_innings, all_batting, all_bowling, all_fielding, all_extras = [], [], [], [], [], []

    for match_id in pending_ids:
        match_data = fetch_match_data(match_id)
        if match_data:
            matches, innings, batting, bowling, fielding, extras = parse_match_data(match_data)
            all_matches.extend(matches)
            all_innings.extend(innings)
            all_batting.extend(batting)
            all_bowling.extend(bowling)
            all_fielding.extend(fielding)
            all_extras.extend(extras)

    # Fetch points table separately
    pts_id = "d5a498c8-7596-4b93-8ab0-e0efc3345312"
    pts_data = fetch_points_table(pts_id)

    if all_matches:
        pd.DataFrame(all_matches).to_sql('matches', con=engine, if_exists='append', index=False)
    if all_innings:
        pd.DataFrame(all_innings).to_sql('innings', con=engine, if_exists='append', index=False)
    if all_batting:
        pd.DataFrame(all_batting).to_sql('batting_df', con=engine, if_exists='append', index=False)
    if all_bowling:
        pd.DataFrame(all_bowling).to_sql('bowling_df', con=engine, if_exists='append', index=False)
    if all_fielding:
        pd.DataFrame(all_fielding).to_sql('fielding_df', con=engine, if_exists='append', index=False)
    if all_extras:
        pd.DataFrame(all_extras).to_sql('extras_df', con=engine, if_exists='append', index=False)
    if pts_data:
        pd.DataFrame(pts_data).to_sql('points_table', con=engine, if_exists='replace', index=False)

    print("✅ Successfully updated yesterday's matches!")

if __name__ == "__main__":
    main()
