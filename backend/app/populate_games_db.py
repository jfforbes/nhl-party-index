from app.nhl_api import fetch_all_games_for_season
from app.db import init_games_table, upsert_game, get_all_teams_from_db

def main():
    from time import sleep
    try:
        from tqdm import tqdm
    except ImportError:
        print("tqdm not found")
        def tqdm(x, **kwargs): return x
        
    seasons = [f"{year}{year+1}" for year in range (2017, 2024)]
    team_abbrs = get_all_teams_from_db()
    init_games_table()
    for season in tqdm(seasons, desc ="Seasons"):
        print(f"\n Processing season {season}...")
        for abbr in tqdm(team_abbrs, desc=f"Teams {season}", leave=False):
            print(f" Fetching games for team {abbr}...")
            games_data = fetch_all_games_for_season(abbr, season)
            games = games_data["games"] if isinstance(games_data, dict) and "games" in games_data else games_data
            for game in tqdm(games, desc=f"Games {abbr} {season}", leave=False):
                if game.get("gameType") == 2:
                    upsert_game(game)
    print("Done!")


if __name__ == "__main__":
    main()
