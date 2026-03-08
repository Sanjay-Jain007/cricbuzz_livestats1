import sqlite3

conn = sqlite3.connect("cricket_complete.db")
cursor = conn.cursor()

# -----------------------------
# PLAYER TABLE
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

# -----------------------------
# PLAYER CAREER BATTING
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS player_batting_stats(
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

# -----------------------------
# PLAYER CAREER BOWLING
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS player_bowling_stats(
id INTEGER PRIMARY KEY AUTOINCREMENT,
player_id INTEGER,
format TEXT,
matches INTEGER,
wickets INTEGER,
average REAL,
economy REAL
)
""")

# -----------------------------
# MATCHES
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS matches(
match_id INTEGER PRIMARY KEY,
team1 TEXT,
team2 TEXT,
venue TEXT,
city TEXT,
match_date TEXT,
format TEXT,
winner TEXT,
margin TEXT
)
""")

# -----------------------------
# VENUES
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS venues(
venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
venue_name TEXT,
city TEXT,
country TEXT,
capacity INTEGER
)
""")

# -----------------------------
# BATTING INNINGS
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS batting_innings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
match_id INTEGER,
player_id INTEGER,
player_name TEXT,
runs INTEGER,
balls INTEGER,
fours INTEGER,
sixes INTEGER,
strike_rate REAL
)
""")

# -----------------------------
# BOWLING INNINGS
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS bowling_innings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
match_id INTEGER,
player_id INTEGER,
overs REAL,
runs INTEGER,
wickets INTEGER,
economy REAL
)
""")

# -----------------------------
# PARTNERSHIPS
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS partnerships(
id INTEGER PRIMARY KEY AUTOINCREMENT,
match_id INTEGER,
player1 TEXT,
player2 TEXT,
runs INTEGER,
innings INTEGER
)
""")

conn.commit()
conn.close()

print("Full cricket database created.")
