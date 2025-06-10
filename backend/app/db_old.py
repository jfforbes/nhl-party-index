import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo




'''need to rewrite all this shit'''
# Initialize the SQLite database and create the 'games' table if it doesn't exist
def init_db():
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id TEXT PRIMARY KEY,
            scheduled TEXT,
            home_id TEXT,
            home_name TEXT,
            away_id TEXT,
            away_name TEXT,
            venue_name TEXT,
            status TEXT,
            home_points INTEGER,
            away_points INTEGER,
            season_id TEXT,
            home_timezone TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert a list of games into the database for a given season
def insert_games_into_db(games, season_id):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    for game in games:
        # Only insert games that are finished (status == "closed")
        if game.get("status") == "closed":
            c.execute('''
                INSERT OR IGNORE INTO games (
                    id, scheduled, home_id, home_name, away_id, away_name,
                    venue_name, status, home_points, away_points, season_id, home_timezone
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game["id"],
                game.get("scheduled"),
                game["home"]["id"],
                game["home"].get("name"),
                game["away"]["id"],
                game["away"].get("name"),
                game.get("venue", {}).get("name"),
                game.get("status"),
                game.get("home_points"),
                game.get("away_points"),
                season_id,
                game.get("venue", {}).get("time_zone")
            ))
    conn.commit()
    conn.close()

# Retrieve all games for a given team (as home or away) from the database
def get_games_for_team_from_db(team_id, season_id):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, scheduled, home_id, home_name, away_id, away_name,
               venue_name, status, home_points, away_points, season_id, home_timezone
        FROM games
        WHERE (home_id = ? OR away_id = ?) AND season_id = ?
        ORDER BY scheduled
    ''', (team_id, team_id, season_id))
    games = c.fetchall()
    conn.close()
    # Convert the result rows into a list of dictionaries for easier use
    return [
        {
            "id": row[0],
            "scheduled": row[1],
            "scheduled_local": utc_to_local(row[1], row[11]) if row[11] else None, 
            "home_id": row[2],
            "home_name": row[3],
            "away_id": row[4],
            "away_name": row[5],
            "venue_name": row[6],
            "status": row[7],
            "home_points": row[8],
            "away_points": row[9],
            "season_id": row[10],
            "home_timezone": row[11]
        }
        for row in games
    ]
    
def get_game_for_game_id_from_db(game_id):
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, scheduled, home_id, home_name, away_id, away_name,
               venue_name, status, home_points, away_points, season_id, home_timezone
        FROM games
        WHERE id = ?
    ''', (game_id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        return None
    # Convert the result rows into a list of dictionaries for easier use
    return {
            "id": row[0],
            "scheduled": row[1],
            "scheduled_local": utc_to_local(row[1], row[11]) if row[11] else None,
            "home_id": row[2],
            "home_name": row[3],
            "away_id": row[4],
            "away_name": row[5],
            "venue_name": row[6],
            "status": row[7],
            "home_points": row[8],
            "away_points": row[9],
            "season_id": row[10],
            "home_timezone": row[11]
        }
    
def get_games_from_date_from_db(date: str):
    """
    Returns all games that happened on a given date (YYYY-MM-DD) from the DB
    """
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    # scheduled field is in ISO format, so match start of string
    c.execute('''
        SELECT id, scheduled, home_id, home_name, away_id, away_name,
               venue_name, status, home_points, away_points, season_id, home_timezone
        FROM games
        WHERE scheduled LIKE ?
        ORDER BY scheduled
    ''', (f"{date}%",))
    games = c.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "scheduled": row[1],
            "scheduled_local": utc_to_local(row[1], row[11]) if row[11] else None,
            "home_id": row[2],
            "home_name": row[3],
            "away_id": row[4],
            "away_name": row[5],
            "venue_name": row[6],
            "status": row[7],
            "home_points": row[8],
            "away_points": row[9],
            "season_id": row[10],
            "home_timezone": row[11]
        }
        for row in games
    ]
    
def utc_to_local(utc_str, tz_str):
    dt_utc = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%SZ")
    dt_utc = dt_utc.replace(tzinfo=ZoneInfo("UTC"))
    dt_local = dt_utc.astimezone(ZoneInfo(tz_str))
    return dt_local.strftime("%Y-%m-%dT%H:%M:%S%z")

def get_away_record_for_team(team_id, season_id):
    """
    Returns the away record (wins, losses, ot_losses) for a team in a given season.
    """
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        SELECT status, away_points, home_points
        FROM games
        WHERE away_id = ? AND season_id = ? AND status = "closed"
    ''', (team_id, season_id))
    games = c.fetchall()
    conn.close()

    wins = losses = 0

    for status, away_points, home_points in games:
        if away_points > home_points:
            wins += 1
        else:
            losses += 1

    return {"wins": wins, "losses": losses}

def get_home_record_for_team(team_id, season_id):
    """
    Returns the home record (wins, losses, ot_losses) for a team in a given season.
    """
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        SELECT home_points, away_points
        FROM games
        WHERE home_id = ? AND season_id = ? AND status = "closed"
    ''', (team_id, season_id))
    games = c.fetchall()
    conn.close()

    wins = losses = 0
    for home_points, away_points in games:
        if home_points > away_points:
            wins += 1
        else:
            losses += 1
    return {"wins": wins, "losses": losses}

def init_player_ages_table():
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS player_ages (
            player_id TEXT,
            game_date TEXT,
            age INTEGER,
            PRIMARY KEY (player_id, game_date)
        )
    ''')
    conn.commit()
    conn.close()