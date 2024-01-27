import requests

def get_track_details(track_id, token):
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response.json()

def get_audio_features(track_id, token):
    url = f'https://api.spotify.com/v1/audio-features/{track_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response.json()

def recommend_songs_for_mood(mood, token):
    # Define mood criteria with seed genres
    mood_criteria = {
        "happy": {"target_valence": 0.7, "target_energy": 0.8, "limit": 5, "seed_genres": "pop"},
        "angry": {"target_energy": 0.9, "target_tempo": 120, "limit": 5, "seed_genres": "rock"},
        "excited": {"target_tempo": 150, "target_energy": 0.8, "limit": 5, "seed_genres": "electronic,dance"},
        "sad": {"target_valence": 0.2, "target_tempo": 70, "limit": 5, "seed_genres": "blues,soul"},
        "tired": {"target_energy": 0.3, "target_tempo": 60, "limit": 5, "seed_genres": "ambient,classical"},
        "neutral": {"target_valence": 0.5, "target_energy": 0.5, "limit": 5, "seed_genres": "indie"},
        "fear": {"target_valence": 0.2, "target_energy": 0.6, "limit": 5, "seed_genres": "experimental,soundtrack"}
    }

    # Building the query string
    query_params = "&".join([f"{key}={value}" for key, value in mood_criteria[mood].items()])

    # Spotify API endpoint for recommendations
    url = f'https://api.spotify.com/v1/recommendations?{query_params}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        recommendations = response.json()['tracks']
        return [f"{track['name']} by {', '.join(artist['name'] for artist in track['artists'])}" for track in recommendations]
    else:
        return f"Error: {response.status_code}, Details: {response.text}"
