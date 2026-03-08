import streamlit as st
import sqlite3
import pandas as pd

st.title("📊 SQL Cricket Analytics")

conn = sqlite3.connect("cricket.db")

queries = {

"1️⃣ Players who represent India":

"""
SELECT name, role, batting_style, bowling_style
FROM players
WHERE country = 'India';
""",

"2️⃣ Matches played in last few days":

"""
SELECT team1, team2, venue, match_date
FROM matches
ORDER BY match_date DESC
LIMIT 20;
""",

"3️⃣ Top 10 run scorers":

"""
SELECT p.name,
SUM(b.runs) as total_runs,
ROUND(AVG(b.runs),2) as average_runs,
SUM(CASE WHEN b.runs>=100 THEN 1 ELSE 0 END) as centuries
FROM batting_stats b
JOIN players p ON b.player_id=p.player_id
GROUP BY p.player_id
ORDER BY total_runs DESC
LIMIT 10;
""",

"4️⃣ Largest venues":

"""
SELECT venue, COUNT(match_id) as matches_hosted
FROM matches
GROUP BY venue
ORDER BY matches_hosted DESC
LIMIT 10;
""",

"5️⃣ Team wins":

"""
SELECT winner, COUNT(*) as wins
FROM matches
WHERE winner IS NOT NULL
GROUP BY winner
ORDER BY wins DESC;
""",

"6️⃣ Player roles count":

"""
SELECT role, COUNT(*) as total_players
FROM players
GROUP BY role;
""",

"7️⃣ Highest individual score":

"""
SELECT p.name, MAX(b.runs) as highest_score
FROM batting_stats b
JOIN players p ON b.player_id=p.player_id
GROUP BY p.player_id
ORDER BY highest_score DESC
LIMIT 10;
""",

"8️⃣ Series list":

"""
SELECT *
FROM matches
LIMIT 20;
""",

"9️⃣ All-rounders with runs and wickets":

"""
SELECT p.name,
SUM(b.runs) as total_runs,
SUM(w.wickets) as total_wickets
FROM players p
JOIN batting_stats b ON p.player_id=b.player_id
JOIN bowling_stats w ON p.player_id=w.player_id
GROUP BY p.player_id
HAVING total_runs>100 AND total_wickets>10
ORDER BY total_runs DESC;
""",

"🔟 Last 20 matches":

"""
SELECT team1,team2,venue,match_date
FROM matches
ORDER BY match_date DESC
LIMIT 20;
""",

"1️⃣1️⃣ Player performance across formats":

"""
SELECT p.name,
SUM(b.runs) as total_runs,
ROUND(AVG(b.runs),2) as avg_runs
FROM players p
JOIN batting_stats b
ON p.player_id=b.player_id
GROUP BY p.player_id
ORDER BY total_runs DESC
LIMIT 20;
""",

"1️⃣2️⃣ Home vs away":

"""
SELECT team1,
COUNT(*) as matches_played
FROM matches
GROUP BY team1
ORDER BY matches_played DESC;
""",

"1️⃣3️⃣ Partnerships over 100":

"""
SELECT player1,player2,runs
FROM partnerships
WHERE runs>=100
ORDER BY runs DESC;
""",

"1️⃣4️⃣ Bowler venue performance":

"""
SELECT p.name,
SUM(w.wickets) as wickets,
ROUND(AVG(w.economy),2) as economy
FROM bowling_stats w
JOIN players p
ON w.player_id=p.player_id
GROUP BY p.player_id
ORDER BY wickets DESC
LIMIT 15;
""",

"1️⃣5️⃣ Close match players":

"""
SELECT p.name,
AVG(b.runs) as avg_runs
FROM batting_stats b
JOIN players p
ON b.player_id=p.player_id
GROUP BY p.player_id
ORDER BY avg_runs DESC
LIMIT 20;
""",

"1️⃣6️⃣ Player yearly performance":

"""
SELECT p.name,
COUNT(b.match_id) as matches,
ROUND(AVG(b.runs),2) as avg_runs
FROM batting_stats b
JOIN players p
ON b.player_id=p.player_id
GROUP BY p.player_id
ORDER BY matches DESC
LIMIT 20;
""",

"1️⃣7️⃣ Toss advantage":

"""
SELECT winner,
COUNT(*) as wins
FROM matches
GROUP BY winner
ORDER BY wins DESC;
""",

"1️⃣8️⃣ Economical bowlers":

"""
SELECT p.name,
ROUND(AVG(w.economy),2) as economy,
SUM(w.wickets) as wickets
FROM bowling_stats w
JOIN players p
ON w.player_id=p.player_id
GROUP BY p.player_id
ORDER BY economy ASC
LIMIT 10;
""",

"1️⃣9️⃣ Consistent batsmen":

"""
SELECT p.name,
AVG(b.runs) as avg_runs
FROM batting_stats b
JOIN players p
ON b.player_id=p.player_id
GROUP BY p.player_id
ORDER BY avg_runs DESC
LIMIT 20;
""",

"2️⃣0️⃣ Matches per player":

"""
SELECT p.name,
COUNT(b.match_id) as matches
FROM batting_stats b
JOIN players p
ON b.player_id=p.player_id
GROUP BY p.player_id
ORDER BY matches DESC
LIMIT 20;
""",

"2️⃣1️⃣ Performance ranking":

"""
SELECT p.name,
SUM(b.runs) as runs,
SUM(w.wickets) as wickets
FROM players p
LEFT JOIN batting_stats b
ON p.player_id=b.player_id
LEFT JOIN bowling_stats w
ON p.player_id=w.player_id
GROUP BY p.player_id
ORDER BY runs+wickets DESC
LIMIT 20;
""",

"2️⃣2️⃣ Head to head":

"""
SELECT team1,team2,
COUNT(*) as matches
FROM matches
GROUP BY team1,team2
ORDER BY matches DESC;
""",

"2️⃣3️⃣ Recent form":

"""
SELECT p.name,
AVG(b.runs) as avg_runs
FROM batting_stats b
JOIN players p
ON b.player_id=p.player_id
GROUP BY p.player_id
ORDER BY avg_runs DESC
LIMIT 20;
""",

"2️⃣4️⃣ Best partnerships":

"""
SELECT player1,player2,
AVG(runs) as avg_runs,
MAX(runs) as highest
FROM partnerships
GROUP BY player1,player2
ORDER BY highest DESC
LIMIT 10;
""",

"2️⃣5️⃣ Player performance trend":

"""
SELECT p.name,
AVG(b.runs) as avg_runs,
COUNT(b.match_id) as matches
FROM batting_stats b
JOIN players p
ON b.player_id=p.player_id
GROUP BY p.player_id
ORDER BY avg_runs DESC
LIMIT 20;
"""

}

query_choice = st.selectbox(
"Select SQL Query",
list(queries.keys())
)

if st.button("Run Query"):

    df = pd.read_sql_query(queries[query_choice], conn)

    st.dataframe(df)

conn.close()
