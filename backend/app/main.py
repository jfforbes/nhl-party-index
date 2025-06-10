from app.utils import get_player_age_on_gameday, get_away_player_ages_for_game, get_days_from_last_game_for_away_team
from app.party_index import get_ypr_for_away_team, get_party_index
from app.db import get_all_game_dates_for_team, get_game_for_game_id_from_db, get_games_from_date, get_player_age_on_gameday_from_db, get_all_game_dates_from_db
from app.nhl_api import fetch_all_games_for_season, fetch_all_team_abbrs, fetch_boxscore, fetch_player_stats, fetch_player_birthdate

from fastapi import FastAPI  # Import the FastAPI class from the fastapi library
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()  # Create an instance of the FastAPI application

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://jfforbes.github.io"],  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_root():
    # Return a simple JSON response as a Python dictionary
    return {"message": "Welcome to the NHL Party Index API"}

@app.get("/get-party-index-for-games/{date}")
def test_party_index(date: str):
    games = get_games_from_date(date)
    party_indexes = []
    for game in games:
        party_indexes.append(get_party_index(game["id"]))
    return party_indexes

@app.get("/get-game/{game_id}")
def get_game(game_id: str):
    return get_game_for_game_id_from_db(game_id)

@app.get("/get-games-from-date/{date}")
def get_games(date: str):
    print(f"Received request for date: {date}")
    return get_games_from_date(date)

'''endpoints I created for testing purposes'''
@app.get("/test-games/{season}")
def games_for_season(season: str):
    print(f"Looking at games for season {season}")
    return fetch_all_games_for_season("BUF", season)

@app.get("/test-teams")
def get_teams():
    print("Looking for list of teams")
    return fetch_all_team_abbrs

@app.get("/test-boxscore/{game_id}")
def get_boxscore(game_id):
    return fetch_boxscore(game_id)

@app.get("/test-player-stats/{player_id}")
def get_player_stats(player_id):
    return fetch_player_stats(player_id)

@app.get("/test-player-birthdate/{player_id}")
def get_player_birthdate(player_id):
    return fetch_player_birthdate(player_id)

@app.get("/test-player-age/{game_id}/{player_id}")
def get_player_age(game_id, player_id):
    return get_player_age_on_gameday(game_id, player_id)

@app.get("/test-away-player-ages-for-game/{game_id}")
def get_player_ages_for_game(game_id):
    return get_away_player_ages_for_game(game_id)

@app.get("/test-ypr-for-team/{game_id}")
def get_ypr_for_away_team(game_id):
    return get_ypr_for_away_team(game_id)

@app.get("/test-game-dates-for-team/{team_id}/{season}")
def get_away_games(team_id, season):
    return get_all_game_dates_for_team(team_id, season)

@app.get("/test-days-from-last-game/{game_id}")
def get_games_between_for_away(game_id):
    return get_days_from_last_game_for_away_team(game_id)

@app.get("/test-player-ages-db/{game_id}/{player_id}")
def get_player_age(game_id, player_id):
    return get_player_age_on_gameday_from_db(game_id, player_id)

@app.get("/get-all-game-dates")
def get_all_game_dates():
    return get_all_game_dates_from_db()
