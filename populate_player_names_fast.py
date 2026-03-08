import requests
import sqlite3
import time
import string

API_KEY = "121e6fbc23msh7da752303c4bf8dp1377c5jsn12cfc3cfda4f"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

letters = list(string.ascii_uppercase)

updated = 0

for letter in letters:

    print("\nSearching:", letter)

    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search?plrN={letter}"

    retries = 3

    while retries > 0:

        try:

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                break

            print("API error:", response.status_code)
            retries -= 1
            time.sleep(2)

        except:
            retries -= 1
            time.sleep(2)

    if retries == 0:
        print("Skipping letter:", letter)
        continue

    data = response.json()

    for player in data.get("player", []):

        player_id = player.get("id")
        name = player.get("name")

        cursor.execute("""
        UPDATE players
        SET name=?
        WHERE player_id=?
        """, (name, player_id))

        if cursor.rowcount > 0:
            print("Updated:", name)
            updated += 1

    time.sleep(0.5)

conn.commit()

print("\nTotal players updated:", updated)

conn.close()
