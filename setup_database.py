import sqlite3

conn = sqlite3.connect("cricket_analytics.db")
cursor = conn.cursor()

# -------------------------
# PLAYERS TABLE
# -------------------------

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

# -------------------------
# MATCHES TABLE
# -------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS matches(
    match_id INTEGER PRIMARY KEY,
    team1 TEXT,
    team2 TEXT,
    venue TEXT,
    city TEXT,
    match_date TEXT,
    format TEXT
)
""")

# -------------------------
# BATTING STATS
# -------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS batting_stats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    match_id INTEGER,
    runs INTEGER,
    balls INTEGER,
    fours INTEGER,
    sixes INTEGER
)
""")

# -------------------------
# BOWLING STATS
# -------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS bowling_stats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    match_id INTEGER,
    overs REAL,
    runs INTEGER,
    wickets INTEGER,
    economy REAL
)
""")

# -------------------------
# FIELDING STATS
# -------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS fielding_stats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    match_id INTEGER,
    catches INTEGER,
    stumpings INTEGER,
    runouts INTEGER
)
""")

# -------------------------
# PARTNERSHIPS
# -------------------------

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

print("Database and tables created successfully.")
