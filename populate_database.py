import requests
import sqlite3

# -----------------------------
# API CONFIG
# -----------------------------

API_KEY = "934d91cdeemshffc3a97c2dd9116p1f7173jsnc99693c4fc73"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

# -----------------------------
# DATABASE
# -----------------------------

conn = sqlite3.connect("cricket.db")
cursor = conn.cursor()

# -----------------------------
# CREATE TABLES
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS matches(
match_id INTEGER PRIMARY KEY,
team1 TEXT,
team2 TEXT,
venue TEXT,
match_date TEXT,
result TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS batting_stats(
id INTEGER PRIMARY KEY AUTOINCREMENT,
player_id INTEGER,
player_name TEXT,
match_id INTEGER,
runs INTEGER,
balls INTEGER,
fours INTEGER,
sixes INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bowling_stats(
id INTEGER PRIMARY KEY AUTOINCREMENT,
player_id INTEGER,
player_name TEXT,
match_id INTEGER,
overs REAL,
runs INTEGER,
wickets INTEGER,
economy REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS partnerships(
id INTEGER PRIMARY KEY AUTOINCREMENT,
match_id INTEGER,
player1 TEXT,
player2 TEXT,
runs INTEGER
)
""")

conn.commit()

# -----------------------------
# FETCH RECENT MATCHES
# -----------------------------

print("Fetching matches...")

url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"

response = requests.get(url, headers=headers)
data = response.json()

match_ids = []

for type_match in data.get("typeMatches", []):
    for series in type_match.get("seriesMatches", []):

        wrapper = series.get("seriesAdWrapper")

        if not wrapper:
            continue

        for match in wrapper.get("matches", []):

            info = match.get("matchInfo")

            match_id = info["matchId"]
            team1 = info["team1"]["teamName"]
            team2 = info["team2"]["teamName"]
            venue = info["venueInfo"]["ground"]
            date = info["startDate"]

            cursor.execute("""
            INSERT OR IGNORE INTO matches VALUES(?,?,?,?,?,?)
            """, (
                match_id,
                team1,
                team2,
                venue,
                date,
                None
            ))

            match_ids.append(match_id)

conn.commit()

print("Matches stored:", len(match_ids))

# -----------------------------
# FETCH SCORECARDS
# -----------------------------

for match_id in match_ids:

    print("Processing match:", match_id)

    score_url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"

    response = requests.get(score_url, headers=headers)

    if response.status_code != 200:
        print("Scorecard API error")
        continue

    score = response.json()

    if "scorecard" not in score:
        print("Scorecard not available")
        continue

    innings_list = score["scorecard"]

    for innings in innings_list:

        # ----------------
        # BATTING
        # ----------------

        for bat in innings.get("batsman", []):

            cursor.execute("""
            INSERT INTO batting_stats(
            player_id,player_name,match_id,runs,balls,fours,sixes
            )
            VALUES(?,?,?,?,?,?,?)
            """, (
                bat.get("id"),
                bat.get("name"),
                match_id,
                bat.get("runs", 0),
                bat.get("balls", 0),
                bat.get("fours", 0),
                bat.get("sixes", 0)
            ))

        # ----------------
        # BOWLING
        # ----------------

        for bowl in innings.get("bowler", []):

            cursor.execute("""
            INSERT INTO bowling_stats(
            player_id,player_name,match_id,overs,runs,wickets,economy
            )
            VALUES(?,?,?,?,?,?,?)
            """, (
                bowl.get("id"),
                bowl.get("name"),
                match_id,
                bowl.get("overs", 0),
                bowl.get("runs", 0),
                bowl.get("wickets", 0),
                bowl.get("economy", 0)
            ))

        # ----------------
        # PARTNERSHIPS
        # ----------------

        partnerships = innings.get("partnership", {}).get("partnership", [])

        for p in partnerships:

            cursor.execute("""
            INSERT INTO partnerships(
            match_id,player1,player2,runs
            )
            VALUES(?,?,?,?)
            """, (
                match_id,
                p.get("bat1name"),
                p.get("bat2name"),
                p.get("totalruns", 0)
            ))

conn.commit()

print("Database population complete")

conn.close()
