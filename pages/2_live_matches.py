import streamlit as st
import requests

st.title("⚡ Live Matches")

# Auto refresh every 15 seconds
st_autorefresh(interval=15000, key="refresh")

API_KEY = "121e6fbc23msh7da752303c4bf8dp1377c5jsn12cfc3cfda4f"

headers = {
    "X-RapidAPI-Key":API_KEY ,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

live_url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

response = requests.get(live_url, headers=headers)


if response.status_code != 200:
    st.error("Failed to fetch matches from API")
    st.stop()

data = response.json()

# SAFETY CHECK
if "typeMatches" not in data:
    st.error("API returned unexpected data. Check your API key or quota.")
    st.json(data)
    st.stop()

matches = {}
scores = {}

for type_match in data["typeMatches"]:
    for series in type_match.get("seriesMatches", []):

        if "seriesAdWrapper" in series:

            for match in series["seriesAdWrapper"].get("matches", []):

                info = match.get("matchInfo", {})
                score = match.get("matchScore", {})

                team1 = info.get("team1", {}).get("teamName", "Team1")
                team2 = info.get("team2", {}).get("teamName", "Team2")

                match_name = f"{team1} vs {team2}"

                matches[match_name] = info
                scores[match_name] = score

if not matches:
    st.warning("No live matches available right now")
    st.stop()

selected_match = st.selectbox(
    "Select Live Match",
    list(matches.keys())
)

match_info = matches[selected_match]
match_score = scores[selected_match]

st.divider()

st.header(selected_match)

col1, col2 = st.columns(2)

with col1:
    st.write("**Series:**", match_info.get("seriesName"))
    st.write("**Match:**", match_info.get("matchDesc"))
    st.write("**Format:**", match_info.get("matchFormat"))

with col2:
    st.write("**Status:**", match_info.get("status"))
    st.write("**Venue:**", match_info.get("venueInfo", {}).get("ground"))
    st.write("**City:**", match_info.get("venueInfo", {}).get("city"))

st.divider()

st.subheader("📊 Current Score")

team1 = match_info.get("team1", {}).get("teamName", "Team1")
team2 = match_info.get("team2", {}).get("teamName", "Team2")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {team1}")

    try:
        t1 = match_score["team1Score"]["inngs1"]
        st.success(f"{t1['runs']}/{t1['wickets']} ({t1['overs']} overs)")
    except:
        st.info("Score not available")

with col2:
    st.markdown(f"### {team2}")

    try:
        t2 = match_score["team2Score"]["inngs1"]
        st.success(f"{t2['runs']}/{t2['wickets']} ({t2['overs']} overs)")
    except:
        st.info("Score not available")

st.divider()

st.subheader("📢 Match Status")

st.info(match_info.get("status"))
