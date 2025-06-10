import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

# initialize the teams table in the db
def init_teams_table():
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            abbreviation TEXT PRIMARY KEY
        )          
    ''')
    conn.commit()
    conn.close()
   
# upsert teams abbrevs from the api into DB
def upsert_teams(team_abbrs):
    """
    teams: list of team abbreviations (strings)
    """
    conn=sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    for abbr in team_abbrs:
        c.execute('''
            INSERT OR REPLACE INTO teams (abbreviation)
            VALUES (?)
        ''', (abbr,))
    conn.commit()
    conn.close()

# get all teams abbrevs from the db
def get_all_teams_from_db():
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('SELECT abbreviation FROM teams')
    teams = [row[0] for row in c.fetchall()]
    conn.close()
    return teams

# initialize the games table in the db
def init_games_table():
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            season INTEGER,
            gameType INTEGER,
            gameDate TEXT,
            venue TEXT,
            neutralSite BOOLEAN,
            startTimeUTC TEXT,
            easternUTCOffset TEXT,
            venueUTCOffset TEXT,
            venueTimezone TEXT,
            gameState TEXT,
            gameScheduleState TEXT,
            awayTeam_id INTEGER,
            awayTeam_abbrev TEXT,
            awayTeam_score INTEGER,
            homeTeam_id INTEGER,
            homeTeam_abbrev TEXT,
            homeTeam_score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# add a game
def upsert_game(game):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO games (
            id, season, gameType, gameDate, venue, neutralSite, startTimeUTC,
            easternUTCOffset, venueUTCOffset, venueTimezone, gameState, gameScheduleState,
            awayTeam_id, awayTeam_abbrev, awayTeam_score,
            homeTeam_id, homeTeam_abbrev, homeTeam_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        game.get("id"),
        game.get("season"),
        game.get("gameType"),
        game.get("gameDate"),
        game.get("venue", {}).get("default"),
        int(game.get("neutralSite", False)),
        game.get("startTimeUTC"),
        game.get("easternUTCOffset"),
        game.get("venueUTCOffset"),
        game.get("venueTimezone"),
        game.get("gameState"),
        game.get("gameScheduleState"),
        game.get("awayTeam", {}).get("id"),
        game.get("awayTeam", {}).get("abbrev"),
        game.get("awayTeam", {}).get("score"),
        game.get("homeTeam", {}).get("id"),
        game.get("homeTeam", {}).get("abbrev"),
        game.get("homeTeam", {}).get("score")
    ))
    conn.commit()
    conn.close()

# initialize players for the away team for each game id table
def init_away_player_ids_table():
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS away_player_ids (
            game_id INTEGER,
            player_id TEXT,
            position TEXT,
            PRIMARY KEY (game_id, player_id)
        )
    ''')
    conn.commit()
    conn.close()
   
# insert an away player into the table
def insert_away_player_id(game_id, player_id, position):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO away_player_ids (game_id, player_id, position)
        VALUES (?, ?, ?)
    ''', (game_id, player_id, position))
    conn.commit()
    conn.close()
   
# get all game ids for all games 
def get_all_game_ids_from_db():
    """
    Returns a list of all game IDs in the games table.
    """
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('SELECT id FROM games')
    game_ids = [row[0] for row in c.fetchall()]
    conn.close()
    return game_ids

# get all game dates from DB
def get_all_game_dates_from_db():
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('SELECT gameDate FROM games')
    game_dates = [row[0] for row in c.fetchall()]
    conn.close()
    return game_dates

# get all games on a date
def get_games_from_date(date: str):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, season, gameType, gameDate, venue, neutralSite, startTimeUTC,
               easternUTCOffset, venueUTCOffset, venueTimezone, gameState, gameScheduleState,
               awayTeam_id, awayTeam_abbrev, awayTeam_score,
               homeTeam_id, homeTeam_abbrev, homeTeam_score
        FROM games WHERE gameDate = ?
    ''', (date,))
    rows = c.fetchall()
    conn.close()
    games = []
    for row in rows:
        games.append({
            "id": row[0],
            "season": row[1],
            "gameType": row[2],
            "gameDate": row[3],
            "venue": row[4],
            "neutralSite": row[5],
            "startTimeUTC": row[6],
            "easternUTCOffset": row[7],
            "venueUTCOffset": row[8],
            "venueTimezone": row[9],
            "gameState": row[10],
            "gameScheduleState": row[11],
            "awayTeam_id": row[12],
            "awayTeam_abbrev": row[13],
            "awayTeam_score": row[14],
            "homeTeam_id": row[15],
            "homeTeam_abbrev": row[16],
            "homeTeam_score": row[17]
        })
    return games
    
# get a single game from the db based on the game id
def get_game_date_from_db(game_id):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('SELECT gameDate FROM games WHERE id = ?', (game_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

# get the away player ids for a game
def get_away_player_ids_for_game(game_id):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('SELECT player_id FROM away_player_ids WHERE game_id = ?', (game_id,))
    player_ids = [row[0] for row in c.fetchall()]
    conn.close()
    return player_ids

# get all the game dates for a team in a season
def get_all_game_dates_for_team(team_id, season):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('SELECT gameDate FROM games WHERE (awayTeam_id = ? or homeTeam_id = ?) AND season = ?', (team_id, team_id, season,))
    game_dates = [row[0] for row in c.fetchall()]
    conn.close()
    return game_dates

# get game information from a game_id
def get_game_for_game_id_from_db(game_id):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, season, gameType, gameDate, venue, neutralSite, startTimeUTC,
               easternUTCOffset, venueUTCOffset, venueTimezone, gameState, gameScheduleState,
               awayTeam_id, awayTeam_abbrev, awayTeam_score,
               homeTeam_id, homeTeam_abbrev, homeTeam_score
        FROM games WHERE id = ?
    ''', (game_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "season": row[1],
        "gameType": row[2],
        "gameDate": row[3],
        "venue": row[4],
        "neutralSite": row[5],
        "startTimeUTC": row[6],
        "easternUTCOffset": row[7],
        "venueUTCOffset": row[8],
        "venueTimezone": row[9],
        "gameState": row[10],
        "gameScheduleState": row[11],
        "awayTeam_id": row[12],
        "awayTeam_abbrev": row[13],
        "awayTeam_score": row[14],
        "homeTeam_id": row[15],
        "homeTeam_abbrev": row[16],
        "homeTeam_score": row[17]
    }
    
def get_all_games_for_team_from_db(team_abbrev, season):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, season, gameType, gameDate, venue, neutralSite, startTimeUTC,
               easternUTCOffset, venueUTCOffset, venueTimezone, gameState, gameScheduleState,
               awayTeam_id, awayTeam_abbrev, awayTeam_score,
               homeTeam_id, homeTeam_abbrev, homeTeam_score
        FROM games WHERE (awayTeam_abbrev = ? OR homeTeam_abbrev = ?) AND season = ?
    ''', (team_abbrev, team_abbrev, season,))
    rows = c.fetchall()
    conn.close()
    games = []
    for row in rows:
        games.append ( {
            "id": row[0],
            "season": row[1],
            "gameType": row[2],
            "gameDate": row[3],
            "venue": row[4],
            "neutralSite": row[5],
            "startTimeUTC": row[6],
            "easternUTCOffset": row[7],
            "venueUTCOffset": row[8],
            "venueTimezone": row[9],
            "gameState": row[10],
            "gameScheduleState": row[11],
            "awayTeam_id": row[12],
            "awayTeam_abbrev": row[13],
            "awayTeam_score": row[14],
            "homeTeam_id": row[15],
            "homeTeam_abbrev": row[16],
            "homeTeam_score": row[17]
        })
    return games

def get_away_games_for_team_from_db(team_id, season):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, season, gameType, gameDate, venue, neutralSite, startTimeUTC,
               easternUTCOffset, venueUTCOffset, venueTimezone, gameState, gameScheduleState,
               awayTeam_id, awayTeam_abbrev, awayTeam_score,
               homeTeam_id, homeTeam_abbrev, homeTeam_score
        FROM games WHERE awayTeam_id = ? AND season = ?
    ''', (team_id, season,))
    rows = c.fetchall()
    conn.close()
    games = []
    for row in rows:
        games.append ( {
            "id": row[0],
            "season": row[1],
            "gameType": row[2],
            "gameDate": row[3],
            "venue": row[4],
            "neutralSite": row[5],
            "startTimeUTC": row[6],
            "easternUTCOffset": row[7],
            "venueUTCOffset": row[8],
            "venueTimezone": row[9],
            "gameState": row[10],
            "gameScheduleState": row[11],
            "awayTeam_id": row[12],
            "awayTeam_abbrev": row[13],
            "awayTeam_score": row[14],
            "homeTeam_id": row[15],
            "homeTeam_abbrev": row[16],
            "homeTeam_score": row[17]
        })
    return games

def get_home_games_for_team_from_db(team_id, season):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, season, gameType, gameDate, venue, neutralSite, startTimeUTC,
               easternUTCOffset, venueUTCOffset, venueTimezone, gameState, gameScheduleState,
               awayTeam_id, awayTeam_abbrev, awayTeam_score,
               homeTeam_id, homeTeam_abbrev, homeTeam_score
        FROM games WHERE homeTeam_id = ? AND season = ?
    ''', (team_id, season,))
    rows = c.fetchall()
    conn.close()
    games = []
    for row in rows:
        games.append ( {
            "id": row[0],
            "season": row[1],
            "gameType": row[2],
            "gameDate": row[3],
            "venue": row[4],
            "neutralSite": row[5],
            "startTimeUTC": row[6],
            "easternUTCOffset": row[7],
            "venueUTCOffset": row[8],
            "venueTimezone": row[9],
            "gameState": row[10],
            "gameScheduleState": row[11],
            "awayTeam_id": row[12],
            "awayTeam_abbrev": row[13],
            "awayTeam_score": row[14],
            "homeTeam_id": row[15],
            "homeTeam_abbrev": row[16],
            "homeTeam_score": row[17]
        })
    return games

def get_player_age_on_gameday_from_db(game_id, player_id):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''SELECT age from away_player_ids WHERE game_id = ? AND player_id = ?
              ''', (game_id, player_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_party_index_from_db(game_id):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute("SELECT party_index from games WHERE id = ?", (game_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_games_with_party_index(party_index):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, season, gameType, gameDate, venue, neutralSite, startTimeUTC,
               easternUTCOffset, venueUTCOffset, venueTimezone, gameState, gameScheduleState,
               awayTeam_id, awayTeam_abbrev, awayTeam_score,
               homeTeam_id, homeTeam_abbrev, homeTeam_score
        FROM games WHERE party_index > ?
    ''', (party_index,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "season": row[1],
        "gameType": row[2],
        "gameDate": row[3],
        "venue": row[4],
        "neutralSite": row[5],
        "startTimeUTC": row[6],
        "easternUTCOffset": row[7],
        "venueUTCOffset": row[8],
        "venueTimezone": row[9],
        "gameState": row[10],
        "gameScheduleState": row[11],
        "awayTeam_id": row[12],
        "awayTeam_abbrev": row[13],
        "awayTeam_score": row[14],
        "homeTeam_id": row[15],
        "homeTeam_abbrev": row[16],
        "homeTeam_score": row[17]
    }