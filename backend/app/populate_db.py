# Import the Sportsradar API helper and database functions
import app.nhl_api
from app.db import init_teams_table, upsert_teams, get_all_teams_from_db

'''fix later
def main():
    # Initialize the SQLite database and create tables if they don't exist
    init_db()
    # Generate a list of season IDs as strings from 2016 to 2024 (inclusive)
    season_ids = [str(year) for year in range(2016, 2025)]
    # Loop through each season and attempt to fetch and insert games
    for season_id in season_ids:
        try:
            # Fetch all games for the given season from the Sportsradar API
            games = app.nhl_api.fetch_all_games_for_season(season_id)
            # Insert the fetched games into the database with the season ID
            insert_games_into_db(games, season_id)
            print(f"Inserted games for season {season_id}")
        except Exception as e:
            # If there is an error (e.g., season not found), print a message and skip
            print(f"Skipping season {season_id:}: {e}")
'''

def main(): 
    init_teams_table()
    abbrs = app.nhl_api.fetch_all_team_abbrs()
    print(abbrs)
    upsert_teams(abbrs)
    print(get_all_teams_from_db())   
        
# Only run the main function if this script is executed directly (not imported)
if __name__ == "__main__":
    main()
    


