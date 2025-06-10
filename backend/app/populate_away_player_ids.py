from app.db import (
    init_away_player_ids_table,
    insert_away_player_id,
    get_all_game_ids_from_db,
)
from app.nhl_api import fetch_boxscore

def main():
    from time import sleep
    try:
        from tqdm import tqdm
    except ImportError:
        print("tqdm not found")
        def tqdm(x, **kwargs): return x
        
    init_away_player_ids_table()
    game_ids = get_all_game_ids_from_db()

    for game_id in tqdm(game_ids, desc="Games"):
        for attempt in range(3):
            try:
                boxscore = fetch_boxscore(game_id)
                players = boxscore.get("playerByGameStats", {})
                away = players.get("awayTeam", {})
                for pos in ["forwards", "defense", "goalies"]:
                    for player in away.get(pos, []):
                        insert_away_player_id(game_id, player["playerId"], pos)
                break #exit retry loop
            except Exception as e:
                if attempt < 2:
                    print(f"Error processing game {game_id} (attempt {attempt+1}/3): {e}. Retrying...")
                else:
                    print(f"Error processing game {game_id}: {e}")
            
    print("Done!")
    
if __name__ == "__main__":
    main()