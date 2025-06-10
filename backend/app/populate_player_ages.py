import sqlite3
from app.utils import get_player_age_on_gameday
from tqdm import tqdm

def update_away_player_ages():
    conn = sqlite3.connect('nhl_schedule.db')
    c = conn.cursor()
    c.execute("SELECT game_id, player_id FROM away_player_ids")
    rows = c.fetchall()
    for game_id, player_id in tqdm(rows, desc="Updating player ages..."):
        c.execute(
            "SELECT age FROM away_player_ids WHERE game_id = ? AND player_id = ?",
            (game_id, player_id,)
            )
        result = c.fetchone()
        if result is not None:
            age = result[0]
        else:
            age = None
        if age is None:
            age = get_player_age_on_gameday(game_id, player_id)
            if age is not None:
                c.execute(
                    "UPDATE away_player_ids SET age = ? WHERE game_id = ? AND player_id = ?",
                    (age, game_id, player_id)
                )
                conn.commit()
    
    conn.close()
    
if __name__ == "__main__":
    update_away_player_ages()