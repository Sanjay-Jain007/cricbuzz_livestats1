import requests
import sqlite3
import time

API_KEY = "934d91cdeemshffc3a97c2dd9116p1f7173jsnc99693c4fc73"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

# -----------------------------
# GET UNIQUE PLAYER IDS
# -----------------------------

player_ids = set()

cursor.execute("SELECT DISTINCT player_id FROM batting_stats")
for row in cursor.fetchall():
    player_ids.add(row[0])

cursor.execute("SELECT DISTINCT player_id FROM bowling_stats")
for row in cursor.fetchall():
    player_ids.add(row[0])

print("Total players found in matches:", len(player_ids))

# -----------------------------
# FETCH PLAYER INFO
# -----------------------------

for player_id in player_ids:

    try:

        url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"

        response = requests.get(url, headers=headers)
        print("STATUS:", response.status_code)

        if response.status_code != 200:
            continue

        data = response.json()

        name = data.get("name")
        country = data.get("intlTeam")
        role = data.get("role")
        bat = data.get("bat")
        bowl = data.get("bowl")

        cursor.execute("""
        INSERT OR IGNORE INTO players
        VALUES(?,?,?,?,?,?)
        """, (player_id, name, country, role, bat, bowl))

        print("Inserted player:", name)

        time.sleep(0.2)

    except:
        continue

conn.commit()

print("Players inserted successfully")

conn.close()
