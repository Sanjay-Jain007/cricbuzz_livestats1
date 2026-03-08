import requests
import sqlite3
import time

# -----------------------
# API CONFIG
# -----------------------

API_KEY = "a53e66769dmsh579120ea76b5543p1ddd62jsn5e70a5629d2d"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

# -----------------------
# DATABASE
# -----------------------

conn = sqlite3.connect("cricket_complete.db")
cursor = conn.cursor()

# -----------------------
# GET RECENT MATCHES
# -----------------------

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
            
            info = match.get("matchInfo", {})
            
            match_id = info.get("matchId")
            team1 = info.get("team1", {}).get("teamName")
            team2 = info.get("team2", {}).get("teamName")
            venue = info.get("venueInfo", {}).get("ground")
            city = info.get("venueInfo", {}).get("city")
            match_date = info.get("startDate")
            match_format = info.get("matchFormat")
            
            cursor.execute("""
            INSERT OR IGNORE INTO matches
            VALUES(?,?,?,?,?,?,?,?,?)
            """, (
                match_id,
                team1,
                team2,
                venue,
                city,
                match_date,
                match_format,
                None,
                None
            ))
            
            match_ids.append(match_id)

conn.commit()

print("Matches stored:", len(match_ids))

# -----------------------
# FETCH SCORECARDS
# -----------------------
for match_id in match_ids:

    print("Processing match:", match_id)

    overs_url = f"https://cricbuzz-cricket.p.rapidapi.com/matches/get-overs?matchId={match_id}"

    response = requests.get(overs_url, headers=headers)

    if response.status_code != 200:
        print("API error:", response.status_code)
        continue

    data = response.json()

    if "overs" not in data:
        print("No overs data")
        continue

    overs_list = data["overs"]

    for over in overs_list:

        balls = over.get("balls", [])

        for ball in balls:

            batsman = ball.get("batsmanName")
            bowler = ball.get("bowlerName")
            runs = ball.get("runs", 0)
            wicket = ball.get("isWicket", False)

            # store player
            cursor.execute("""
            INSERT OR IGNORE INTO players(name)
            VALUES(?)
            """, (batsman,))

            # batting record
            cursor.execute("""
            INSERT INTO batting_innings(match_id,player_name,runs)
            VALUES(?,?,?)
            """, (
                match_id,
                batsman,
                runs
            ))

            # bowling record
            cursor.execute("""
            INSERT INTO bowling_innings(match_id,player_name,wickets)
            VALUES(?,?,?)
            """, (
                match_id,
                bowler,
                1 if wicket else 0
            ))

    
    conn.commit()
    
    time.sleep(1)

print("Database population complete")

conn.close()
