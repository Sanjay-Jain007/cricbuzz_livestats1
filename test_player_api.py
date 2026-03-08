import requests

API_KEY = "ff54ce5afdmsh94ef724963d0a2ap1dd8b5jsn6c56bdcaf0b1"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

player_id = 8271

url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"

response = requests.get(url, headers=headers)

print("STATUS:", response.status_code)
print(response.json())
