import requests
import sqlite3
import time

API_KEY = "YOUR_API_KEY"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

# get match ids
cursor.execute("SELECT match_id FROM matches")
match_ids = [row[0] for row in cursor.fetchall()]

print("Matches found:", len(match_ids))

for match_id in match_ids:

    try:

        print("Fetching scorecard:", match_id)

        url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/hscard"

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("API error:", response.status_code)
            continue

        data = response.json()

        for innings in data.get("scorecard", []):

            # batting players
            for batsman in innings.get("batsman", []):

                player_id = batsman.get("id")
                name = batsman.get("name")

                cursor.execute("""
                UPDATE players
                SET name=?
                WHERE player_id=?
                """, (name, player_id))

            # bowling players
            for bowler in innings.get("bowler", []):

                player_id = bowler.get("id")
                name = bowler.get("name")

                cursor.execute("""
                UPDATE players
                SET name=?
                WHERE player_id=?
                """, (name, player_id))

        time.sleep(0.2)

    except Exception as e:
        print("Error:", e)

conn.commit()

print("Player names updated successfully")

conn.close()
