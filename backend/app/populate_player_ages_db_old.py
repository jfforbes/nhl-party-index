import sqlite3
from app.db import init_player_ages_table
from backend.app.nhl_api import fetch_roster_for_game_id, fetch_player_age_on_date
from tqdm import tqdm

def store_player_age_in_db(conn, player_id, game_date, age):
    c = conn.cursor()
    c.execute(
        'INSERT OR REPLACE INTO player_ages (player_id, game_date, age) VALUES (?, ?, ?)',
        (player_id, game_date, age)
    )
    conn.commit()

def get_all_game_ids_and_dates():
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute('SELECT id, scheduled FROM games WHERE status="closed"')
    games = c.fetchall()
    conn.close()
    return games  # List of (game_id, scheduled_date)

def main():
    init_player_ages_table()
    conn = sqlite3.connect('nhl_schedule.db')
    games = get_all_game_ids_and_dates()
    for game_id, scheduled in tqdm(games, desc="Processing games"):
        game_date = scheduled[:10]  # 'YYYY-MM-DD'
        try:
            away_player_ids = fetch_roster_for_game_id(game_id, "away")
            for pid in away_player_ids:
                c = conn.cursor()
                c.execute('SELECT 1 FROM player_ages WHERE player_id=? AND game_date=?', (pid, game_date))
                exists = c.fetchone()
                if exists:
                    continue
                age = fetch_player_age_on_date(game_date, pid, retries=3)
                store_player_age_in_db(conn, pid, game_date, age)
        except Exception as e:
            print(f"Error processing game {game_id}: {e}")
    conn.close()

if __name__ == "__main__":
    main()