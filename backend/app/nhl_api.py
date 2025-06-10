from nhlpy import NHLClient
import requests
from fastapi import HTTPException
import os
# from dotenv import load_dotenv don't need ENV variables anymore
from datetime import  datetime
import time
import httpx

client = NHLClient()

#from app.utils import get_season_id #do I still need this


''' No longer need an API key because the API is public
load_dotenv() #Loads variables from .env file
api_key = os.getenv("SPORTRADAR_API_KEY")

delay_seconds = 1.0 # how many seconds to wait beteween API calls
'''

def fetch_all_team_abbrs():
    '''
    Returns a list of all NHL teams
    Caches
    '''
    teams = client.teams.teams_info()
    abbrs = [team["abbr"] for team in teams]
    return abbrs

def fetch_all_games_for_season(team_abbr:str ,season : str, retries: int  = 3, delay: float = 1.0):
    '''
    Fetch all regular season games for a given NHL season
    season_id should be a string like 20162017 or 20222023
    '''
    for attempt in range(retries):
        try:
            data = client.schedule.get_season_schedule(team_abbr=team_abbr, season=season)
            return data
        except Exception as e:
            print(f"Error fetching games for {team_abbr} {season}: {e}")
        if attempt < retries - 1:
            print(f"Retrying in {delay} seconds...attempt {attempt + 2} out of {retries}")
            time.sleep(delay)
        else:
            print("Max retries reached. Returning empty list")
            return []
    
def fetch_boxscore(game_id: str):
    return client.game_center.boxscore(game_id)

def fetch_player_stats(player_id: str):
    return client.stats.player_career_stats(player_id)

def fetch_player_birthdate(player_id: str, retries: int = 3, delay: float = 5.0):
    for attempt in range(retries):
        try:
            player = client.stats.player_career_stats(player_id)
            return player["birthDate"]
        except httpx.ConnectTimeout:
            print(f"Connect timeout fetching birthday for player_id {player_id} (attempt {attempt+1}/retries)")
            if attempt < retries-1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Returning None")
                return None
        except Exception as e:
            print(f"Error fetching birthday for player {player_id}: {e}")
            return None
    return None

'''DEPRECEATED: needed to switch APIs because I was making too many calls
def fetch_all_games_for_season(season_id: str):
    url = f"https://api.sportradar.us/nhl/trial/v7/en/games/{season_id}/REG/schedule.json?api_key={api_key}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data["games"] #all games
    
    else:
        print("Error fetching data", response.text) # Print error message
        raise HTTPException(status_code=500, detail="Failed to fetch season data from Sportradar")

def fetch_roster_for_game_id(game_id, home_or_away: str, retries = 3):

    url = f"https://api.sportradar.us/nhl/trial/v7/en/games/{game_id}/summary.json?api_key={api_key}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, timeout= 10)
    
    if response.status_code == 200:
        data = response.json()
        roster = data[home_or_away]["players"] # This is a list of player dicts
        roster_ids = [player["id"] for player in roster]
        #player_ages = [get_player_age_on_date("2025-04-14", pid) for pid in roster_ids]
        #  print(get_ypr_for_team(player_ages))
        return roster_ids
    
    # trying again if rate limited
    elif (response.status_code == 429 or "Too Many Requests" in response.text) and retries > 0:
            print(f"Rate limited! Waiting 3 seconds before retrying...({retries} remaining)")
            time.sleep(3)
            return fetch_roster_for_game_id(game_id, home_or_away, retries=retries-1)
    
    else:
        print("Error fetching data", response.text) # Print error message
        raise HTTPException(status_code=500, detail="Failed to fetch roster data from Sportradar")

def fetch_games_for_date(date : str = None):
    # get the season 
    season_id = get_season_id(date)
    
    #build the url and get response
    url = f"https://api.sportradar.us/nhl/trial/v7/en/games/{season_id}/REG/schedule.json?api_key={api_key}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    
    #if the request was successful
    if response.status_code == 200:
        data = response.json() #parse response
        games = data["games"] #extract the list
        
        if date != None:
            filtered_games = []
            for game in games:
                if game["scheduled"].startswith(date):
                    filtered_games.append(game)
            return filtered_games
        else:
            return games
        # return JSON of the games
    #if it wasn't
    else:
        print("Error fetching data", response.text) # Print error message
        raise HTTPException(status_code=500, detail="Failed to fetch season from Sportradar")


def fetch_player_age_on_date(game_date: str, player_id: str, retries):
    """
    Fetches the age of an NHL player on a specific game date using the Sportradar API.
    Args:
        game_date (str): The date of the game in 'YYYY-MM-DD' format.
        player_id (str): The unique identifier of the player.
    Returns:
        int: The age of the player on the specified game date.
    Raises:
        HTTPException: If the API request fails or player data cannot be fetched.
    """
    
    url = f"https://api.sportradar.us/nhl/trial/v7/en/players/{player_id}/profile.json?api_key={api_key}" #42a966db-0f24-11e2-8525-18a905767e44
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        data = response.json()
        dob_str = data["birthdate"]
        
        # create date objects
        dob_int = datetime.strptime(dob_str, "%Y-%m-%d")
        game_date_int = datetime.strptime(game_date, "%Y-%m-%d")
        
        age = game_date_int.year - dob_int.year - ((game_date_int.month, game_date_int.day) < (dob_int.month, dob_int.day))
        
        return age
    # trying again if rate limited
    elif (response.status_code == 429 or "Too Many Requests" in response.text) and retries > 0:
            print(f"Rate limited! Waiting 3 seconds before retrying... ({retries} remaining)")
            time.sleep(3)
            return fetch_player_age_on_date(game_date, player_id, retries = retries - 1)

    #if it was an error
    else:
        print("Error fetching data", response.text) # Print error message
    raise HTTPException(status_code=500, detail="Failed to fetch player data from Sportradar")

def fetch_away_player_ages_for_game(game_id):
    """
    Returns a list of ages for all away players given a game_id
    """
    from app.db import get_game_for_game_id_from_db
    
    game = get_game_for_game_id_from_db(game_id)
    if not game:
        print(f"Game_id: {game_id} not found!")
        return []
    
    game_date = game["scheduled"][:10] # 'YYYY-MM-DD'
    away_player_ids = fetch_roster_for_game_id(game_id, "away")
    ages = []
    for pid in away_player_ids:
        try:
            age = fetch_player_age_on_date(game_date, pid)
            print(f"Age for player: {pid} is {age}")
            ages.append(age)
        except Exception as e:
            print(f"Could not fetch age for player {pid}: {e}")
    return ages
'''