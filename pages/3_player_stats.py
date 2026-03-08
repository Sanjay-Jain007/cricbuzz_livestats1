import streamlit as st
import requests
import sqlite3
import pandas as pd

st.title("🔎 Player Statistics")

API_KEY = "121e6fbc23msh7da752303c4bf8dp1377c5jsn12cfc3cfda4f"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

conn = sqlite3.connect("cricket.db")

# -------------------------
# SEARCH PLAYER (API)
# -------------------------

query = st.text_input("Search Player")

players = {}

if query:

    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search?plrN={query}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        data = response.json()

        for p in data.get("player", []):
            players[p["name"]] = p["id"]

    if players:

        selected_player = st.selectbox(
            "Select Player",
            list(players.keys())
        )

        player_id = players[selected_player]

        # -------------------------
        # PLAYER BASIC INFO (API)
        # -------------------------

        info_url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"

        info_response = requests.get(info_url, headers=headers)

        if info_response.status_code == 200:

            info = info_response.json()

            st.subheader(info.get("name",""))

            colA, colB = st.columns(2)

            with colA:
                st.write("**Country:**", info.get("intlTeam",""))
                st.write("**Role:**", info.get("role",""))

            with colB:
                st.write("**Batting Style:**", info.get("bat",""))
                st.write("**Bowling Style:**", info.get("bowl",""))

        st.divider()

        # -------------------------
        # BATTING STATS (DATABASE)
        # -------------------------

        batting_query = f"""
        SELECT
        COUNT(match_id) as matches,
        SUM(runs) as runs,
        ROUND(AVG(runs),2) as average,
        SUM(CASE WHEN runs >= 100 THEN 1 ELSE 0 END) as centuries,
        SUM(CASE WHEN runs >= 50 THEN 1 ELSE 0 END) as fifties
        FROM batting_stats
        WHERE player_id = {player_id}
        """

        batting = pd.read_sql_query(batting_query, conn)

        # -------------------------
        # BOWLING STATS (DATABASE)
        # -------------------------

        bowling_query = f"""
        SELECT
        SUM(wickets) as wickets,
        ROUND(AVG(economy),2) as economy
        FROM bowling_stats
        WHERE player_id = {player_id}
        """

        bowling = pd.read_sql_query(bowling_query, conn)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Matches", int(batting["matches"][0] or 0))
            st.metric("Runs", int(batting["runs"][0] or 0))

        with col2:
            st.metric("Average", batting["average"][0] or 0)
            st.metric("100s", int(batting["centuries"][0] or 0))

        with col3:
            st.metric("50s", int(batting["fifties"][0] or 0))
            st.metric("Wickets", int(bowling["wickets"][0] or 0))

    else:
        st.warning("No player found")

conn.close()
