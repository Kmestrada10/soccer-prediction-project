import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

API_KEY = os.getenv('RAPIDAPI_KEY')
headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def fetch_season_data(season):
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?league=140&season={season}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed for season {season}: {response.status_code}")
        return None

def fetch_la_liga_data(start_year=2000):
    current_year = datetime.now().year
    for season in range(start_year, current_year + 1):
        print(f"Fetching season {season}...")
        data = fetch_season_data(season)
        if data:
            path = f"../../data/raw/la_liga_{season}.json"
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
            print(f"✅ Season {season} data fetched and saved.")
        else:
            print(f"⚠️ Skipped season {season} due to error.")
        
        # Prevent hitting API limits (Rate limiting)
        time.sleep(5)

if __name__ == "__main__":
    fetch_la_liga_data()
