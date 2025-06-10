from .city_modifiers import city_modifiers #import the list of party city modifiers
from app.utils import get_away_player_ages_for_game, get_days_from_last_game_for_away_team, calculate_away_record
# from backend.app.nhl_api import fetch_away_player_ages_for_game
from app.db import get_game_for_game_id_from_db, get_party_index_from_db
import sqlite3

ypr_age = 28 # age for my young player ratio calculation

#get the ratio of players under 28 to total players on the team, > 1 if there are more than half young players
def get_ypr_for_away_team(game_id) -> float:
    player_ages = get_away_player_ages_for_game(game_id)
    young_players = sum(1 for age in player_ages if age < ypr_age)
    total = len(player_ages)
    ratio = young_players / total if total > 0 else 0
    return float(f"{ratio*2:.2f}")

def get_party_index(game_id):
    print(f"Getting party index for {game_id}")
    game = get_game_for_game_id_from_db(game_id)
    if not game:
        print(f"Game not found, game_id: {game_id}")
        return None
    
    home_team = game["homeTeam_abbrev"]
    away_team = game["awayTeam_abbrev"]
    away_lost = did_away_lose(game)
    season = game["season"]
    away_record = calculate_away_record(game["awayTeam_id"], season)
    
    cached_party_index = get_party_index_from_db(game_id)
    
    if cached_party_index is not None:
        print(f"Party index found in DB for game {game_id}")
        return {
        "party_index": float(cached_party_index),
        "game": game,
        "away_lost": away_lost,
        "away_record": away_record
        }
        
    #get ypr
    ypr = get_ypr_for_away_team(game_id)
    
    #get city modifier
    
    print(f"Getting city modifier for {home_team}") # - used for debug
    city_mod = city_modifiers.get(home_team, 5) #defaults to 5 if not found
    
    days_rest = get_days_from_last_game_for_away_team(game_id)
    if days_rest == None:
        print("Days rest unknown! setting to 2")
        days_rest = 2
        
    isb2b = days_rest == 0
    
    if city_mod < 5:
        rest_multiplier = 0.7 if isb2b else 1.5
    else:
        if isb2b: #no days off, unlikely to party
            rest_multiplier = 1.5
        elif days_rest == 2: #1 day off between games
            rest_multiplier = 1
        else:
            rest_multiplier = 1.5
            
    #calculate party index
    print(f"Calculating party index for game {game_id} at {home_team}: {rest_multiplier} * {ypr} * {city_mod}")
    party_index = rest_multiplier * ypr * city_mod
    party_index *= 10 # make it bigger
    party_index = float(f"{party_index:.2f}")
    
    write_party_index_to_db(game_id, party_index)
            
    return {
        "party_index": party_index,
        "game": game,
        "away_lost": away_lost,
        "away_record": away_record
    }

def did_away_lose(game):
    if game.get("awayTeam_score") is not None and game.get("homeTeam_score") is not None:
        return game["awayTeam_score"] < game["homeTeam_score"]

def write_party_index_to_db(game_id, party_index):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute(
        "UPDATE games SET party_index = ? WHERE id = ?", 
        (party_index, game_id)
    )
    conn.commit()
    conn.close()