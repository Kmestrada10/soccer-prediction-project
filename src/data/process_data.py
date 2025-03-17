import json
import pandas as pd
import glob
import os

def process_all_seasons(raw_data_folder="../../data/raw/", processed_data_folder="../../data/processed/"):
    files = glob.glob(f"{raw_data_folder}/la_liga_*.json")
    all_matches = []

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)

        season = os.path.basename(file).split('_')[-1].split('.')[0]
        print(f"Processing season {season}")

        matches = data.get('response', [])
        for match in matches:
            fixture = match['fixture']
            teams = match['teams']
            goals = match['goals']
            league = match['league']

            match_data = {
                'fixture_id': fixture['id'],
                'date': fixture['date'],
                'season': league['season'],
                'round': league['round'],
                'venue': fixture['venue']['name'],
                'home_team': teams['home']['name'],
                'away_team': teams['away']['name'],
                'home_goals': goals['home'],
                'away_goals': goals['away'],
                'status': fixture['status']['long'],
                'home_team_winner': teams['home']['winner'],
                'away_team_winner': teams['away']['winner'],
                'draw': teams['home']['winner'] is None and teams['away']['winner'] is None
            }

            all_matches.append(match_data)

    df = pd.DataFrame(all_matches)
    os.makedirs(processed_data_folder, exist_ok=True)
    df.to_csv(f"{processed_data_folder}/la_liga_processed.csv", index=False)

    print(f"✅ All seasons processed into la_liga_processed.csv ({df.shape[0]} rows).")

if __name__ == "__main__":
    process_all_seasons()
