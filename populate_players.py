import requests
import sqlite3
import string
import time

# -----------------------------
# API CONFIG
# -----------------------------

API_KEY = "ff54ce5afdmsh94ef724963d0a2ap1dd8b5jsn6c56bdcaf0b1"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

# -----------------------------
# DATABASE CONNECTION
# -----------------------------

conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

# -----------------------------
# CREATE TABLES
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS players(
player_id INTEGER PRIMARY KEY,
name TEXT,
country TEXT,
role TEXT,
batting_style TEXT,
bowling_style TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS player_batting_career(
id INTEGER PRIMARY KEY AUTOINCREMENT,
player_id INTEGER,
format TEXT,
matches INTEGER,
runs INTEGER,
average REAL,
strike_rate REAL,
hundreds INTEGER,
fifties INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS player_bowling_career(
id INTEGER PRIMARY KEY AUTOINCREMENT,
player_id INTEGER,
format TEXT,
matches INTEGER,
wickets INTEGER,
economy REAL,
average REAL
)
""")

conn.commit()

# -----------------------------
# SEARCH PLAYERS A-Z
# -----------------------------

for letter in string.ascii_uppercase:

    print("Fetching players starting with:", letter)

    search_url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"

    response = requests.get(
        search_url,
        headers=headers,
        params={"plrN": letter}
    )

    data = response.json()

    players = data.get("player", [])

    for p in players:

        player_id = p["id"]
        name = p["name"]

        print("Processing:", name)

        # -----------------------------
        # PLAYER INFO
        # -----------------------------

        info_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"

        info = requests.get(info_url, headers=headers).json()

        country = info.get("intlTeam")
        role = info.get("role")
        bat = info.get("bat")
        bowl = info.get("bowl")

        cursor.execute("""
        INSERT OR IGNORE INTO players
        VALUES(?,?,?,?,?,?)
        """, (
            player_id,
            name,
            country,
            role,
            bat,
            bowl
        ))

        # -----------------------------
        # BATTING STATS
        # -----------------------------

        bat_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/batting"

        bat_data = requests.get(bat_url, headers=headers).json()

        for f in bat_data.get("values", []):

            format_name = f.get("format")
            vals = f.get("values", [])

            matches = vals[0] if len(vals) > 0 else 0
            runs = vals[3] if len(vals) > 3 else 0
            avg = vals[5] if len(vals) > 5 else 0
            sr = vals[6] if len(vals) > 6 else 0
            hundreds = vals[8] if len(vals) > 8 else 0
            fifties = vals[9] if len(vals) > 9 else 0

            cursor.execute("""
            INSERT INTO player_batting_career(
            player_id,format,matches,runs,average,strike_rate,hundreds,fifties
            )
            VALUES(?,?,?,?,?,?,?,?)
            """, (
                player_id,
                format_name,
                matches,
                runs,
                avg,
                sr,
                hundreds,
                fifties
            ))

        # -----------------------------
        # BOWLING STATS
        # -----------------------------

        bowl_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/bowling"

        bowl_data = requests.get(bowl_url, headers=headers).json()

        for f in bowl_data.get("values", []):

            format_name = f.get("format")
            vals = f.get("values", [])

            matches = vals[0] if len(vals) > 0 else 0
            wickets = vals[3] if len(vals) > 3 else 0
            avg = vals[4] if len(vals) > 4 else 0
            eco = vals[5] if len(vals) > 5 else 0

            cursor.execute("""
            INSERT INTO player_bowling_career(
            player_id,format,matches,wickets,economy,average
            )
            VALUES(?,?,?,?,?,?)
            """, (
                player_id,
                format_name,
                matches,
                wickets,
                eco,
                avg
            ))

        time.sleep(0.5)

conn.commit()

print("Player database built successfully")

conn.close()
