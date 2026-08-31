import os
import anthropic
import json
import requests
import base64
from dotenv import load_dotenv

# Loading environment variables and retrieving API keys (weather + anthropic)
load_dotenv()
weatherAPI_key = os.getenv("OPEN_WEATHER_API_KEY")
anthropicAPI_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=anthropicAPI_key)
spotifyClientID = os.getenv("SPOTIFY_CLIENT_ID")
spotifyClientSecret = os.getenv("SPOTIFY_CLIENT_SECRET")

# Spotify OAuth (more complicated than other APIs)
joined_spotify_data =f"{spotifyClientID}:{spotifyClientSecret}"
encoded_spotify_data = joined_spotify_data.encode()
b64_encoded_spotify_data = base64.b64encode(encoded_spotify_data)
b64_encoded_spotify_string = b64_encoded_spotify_data.decode()
headers = {"Authorization": f"Basic {b64_encoded_spotify_string}", "Content-Type": "application/x-www-form-urlencoded" }
body = {"grant_type": "client_credentials" }
token_response = requests.post(
    "https://accounts.spotify.com/api/token", 
    headers=headers, 
    data=body)
spotify_data = token_response.json()
spotify_temp_token = spotify_data['access_token']
spotify_call_headers = {"Authorization": f"Bearer {spotify_temp_token}"}


# Obtaining information from user to retrieve weather data
def zip_info(zip_code):
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid={weatherAPI_key}&units=imperial"
    response = requests.get(url)

# Converting data from weather API call into JSON + defining information variables
    data = response.json()
    condition = data['weather'][0]['main']
    temp = data['main']['temp']
    return {"condition": condition, "temp": temp}


# Making AI call, but defining message first for clarity
def get_music_suggestions(condition,temp,mood):
    messages = [
        {"role": "user", "content": f"The weather is {condition} , {temp}, and I'm feeling {mood}. Suggest a music genre that fits this vibe and return the output in only raw JSON, "
        "with the key containing the returned information about music genre being called 'music_genre', the key containing returned information about the vibe being called "
        "'vibe', and the key containing exactly 3 song suggestions based on the music genre and vibe being called 'songs'."}
    ]
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=300,
        messages=messages,
        thinking={"type": "disabled"}
        )

# Using string slicing to obtain only the info from Claude
    start_index = response.content[0].text.find("{")
    stop_index = response.content[0].text.rfind("}")
    json_text = response.content[0].text[start_index:stop_index + 1]

# Converting AI call message to JSON + storing info in variables
    converted_text = json.loads(json_text)
    music_genre = converted_text['music_genre']
    vibe = converted_text['vibe']
    song_suggestions = converted_text['songs']
    return music_genre, vibe, song_suggestions

# Spotify API call for song_suggestions, run through for loop to get each URL preview for the songs
def music_urls(song_suggestions):
    url_list = []
    for song in song_suggestions:
        query_parameters = {
            "q": song,
            "type": "track"
        }
        spotify_song_url = requests.get(
            "https://api.spotify.com/v1/search", 
            params=query_parameters, 
            headers=spotify_call_headers)
    
# JSON returns huge dictionary. Use separate variables to navigate JSON and find track URL for each song
        search_data = spotify_song_url.json()
        tracks_data = search_data['tracks']
        items_list = tracks_data['items']
        first_track = items_list[0]
        track_urls = first_track['external_urls']
        track_link = track_urls['spotify']
        url_list.append(track_link)
    return url_list

# Printing end result
