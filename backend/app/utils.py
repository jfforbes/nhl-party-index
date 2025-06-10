# filepath: backend/app/utils.py

from app.nhl_api import fetch_player_birthdate
from app.db import (
    get_game_for_game_id_from_db, get_away_player_ids_for_game, get_all_game_dates_for_team, 
    get_game_date_from_db, get_all_games_for_team_from_db, get_away_games_for_team_from_db, 
    get_home_games_for_team_from_db, get_player_age_on_gameday_from_db
)
from datetime import datetime
import httpx

def extract_away_player_ids_from_boxscore(boxscore):
    away = boxscore["awayTeam"]
    player_ids = []
    for pos in ["forwards", "defense", "goalies"]:
        for player in away.get(pos, []):
            player_ids.append((player["playerId"], pos))
    return player_ids

def get_player_age_on_gameday(game_id, player_id):
    birthdate_str = fetch_player_birthdate(player_id)
    if not birthdate_str:
        print(f"Birthdate not found for playerId {player_id}")
        return None
    
    game_date_str = get_game_date_from_db(game_id)
    if not game_date_str:
        print(f"gameDate not found for gameID {game_id}")
        return None
    
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    game_date = datetime.strptime(game_date_str, "%Y-%m-%d")
    
    age = int(game_date.year - birthdate.year - ((game_date.month, game_date.day) < (birthdate.month, birthdate.day)))
    return age

def get_away_player_ages_for_game(game_id):
    player_ids = get_away_player_ids_for_game(game_id)
    ages = []
    for player_id in player_ids:
        age = get_player_age_on_gameday_from_db(game_id, player_id)
        # print(f"player id {player_id} age is {age}") - was used to debug
        if age is not None:
            ages.append(int(age))
    return ages

# takes a game_id, calculates when the last game was for a team. 
def get_days_from_last_game_for_away_team(game_id):
    game = get_game_for_game_id_from_db(game_id)
    if not game:
        print("No game found!")
        return None
    
    team_id = game["awayTeam_id"]
    season = game["season"]
    game_date = game["gameDate"]
    
    game_dates = get_all_game_dates_for_team(team_id, season)
    
    if game_date not in game_dates:
        print("Game date not found")
        return None
    idx = game_dates.index(game_date)
    if idx == 0:
        print("No previous game found!")
        return None
    
    prev_game_date = game_dates[idx-1]
    
    date_fmt = "%Y-%m-%d"
    d1 = datetime.strptime(game_date, date_fmt)
    d2 = datetime.strptime(prev_game_date, date_fmt)
    print(f"Info retrieved! Game is {d1}, previous game was {d2}")
    return (d1-d2).days 

def calculate_season_record(team_id, season):
    games = get_all_games_for_team_from_db(team_id, season)
    wins = losses = 0
    for game in games:
        if game["awayTeam_score"] is None or game["homeTeam_score"] is None:
            continue #skip games with missing scores
        if game["awayTeam_score"] > game["homeTeam_score"]:
            wins += 1
        else:
            losses += 1
    
    total_games = wins + losses
    win_pct = wins/total_games*100 if total_games > 0 else 0.0
    win_pct = float(f"{win_pct:.2f}")
    return {"wins": wins, "losses": losses, "win pct": win_pct}
    
def calculate_away_record(team_id, season):
    games = get_away_games_for_team_from_db(team_id, season)
    wins = losses = 0
    for game in games:
        if game["awayTeam_score"] is None or game["homeTeam_score"] is None:
            continue #skip games with missing scores
        if game["awayTeam_score"] > game["homeTeam_score"]:
            wins += 1
        else:
            losses += 1
    
    total_games = wins + losses
    win_pct = wins/total_games*100 if total_games > 0 else 0.0
    win_pct = float(f"{win_pct:.2f}")
    return {"away wins": wins, "away losses": losses, "away win pct": win_pct}
    
    
def calculate_home_record(team_id, season):
    games = get_home_games_for_team_from_db(team_id, season)
    wins = losses = 0
    for game in games:
        if game["awayTeam_score"] is None or game["homeTeam_score"] is None:
            continue #skip games with missing scores
        if game["awayTeam_score"] > game["homeTeam_score"]:
            wins += 1
        else:
            losses += 1
    
    total_games = wins + losses
    win_pct = (wins/total_games)*100 if total_games > 0 else 0.0
    win_pct = float(f"{win_pct:.2f}")
    return {"home wins": wins, "home losses": losses, "home win pct": win_pct}

