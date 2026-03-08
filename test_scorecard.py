import requests

API_KEY = "ff54ce5afdmsh94ef724963d0a2ap1dd8b5jsn6c56bdcaf0b1"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

match_id = 139478

url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/scard"

response = requests.get(url, headers=headers)

print("STATUS:", response.status_code)

data = response.json()

print(data)
