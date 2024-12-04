import requests
from Mydata import client_id, client_secret

# Function to get access token (OAuth)
def get_access_token(client_id, client_secret):
    url = "https://osu.ppy.sh/oauth/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "public"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['access_token']

# Function to get top player rankings
def get_global_rankings(mode, access_token):
    url = f"https://osu.ppy.sh/api/v2/rankings/{mode}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to get replay file for a specific score
def get_replay_file(mode, beatmap_id, score_id, access_token):
    url = f"https://osu.ppy.sh/api/v2/scores/{mode}/{beatmap_id}/{score_id}/download"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Save the replay to a file
    with open(f"replay_{score_id}.osr", "wb") as replay_file:
        replay_file.write(response.content)
    print(f"Replay {score_id} downloaded successfully!")

# Get the access token
access_token = get_access_token(client_id, client_secret)

# Collect top players' rankings
mode = "osu"  # Change as needed (osu, taiko, mania, etc.)
top_players = get_global_rankings(mode, access_token)

# Example: Download a replay for the first top player (replace with actual beatmap_id and score_id)
# For simplicity, we'll assume we want to download the first player's first score.
beatmap_id = top_players['ranking'][0]['scores'][0]['beatmap']['id']
score_id = top_players['ranking'][0]['scores'][0]['id']

# Download the replay file for the first score
get_replay_file(mode, beatmap_id, score_id, access_token)
