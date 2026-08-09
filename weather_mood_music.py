import os
import anthropic
import json
import requests
from dotenv import load_dotenv

# Loading environment variables and retrieving API keys (weather + anthropic)
load_dotenv()
weatherAPI_key = os.getenv("OPEN_WEATHER_API_KEY")
anthropicAPI_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=anthropicAPI_key)

# Obtaining information from user to retrieve weather data
zip_code = input("Please input your zip code: ")
url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid={weatherAPI_key}&units=imperial"
response = requests.get(url)

# Converting data from weather API call into JSON + defining information variables
data = response.json()
condition = data['weather'][0]['main']
temp = data['main']['temp']
mood = input("What vibe are going for today? More specifically, how are you feeling? ")

# Making AI call, but defining message first for clarity
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
songs_sugestions = converted_text['songs']

# Printing end result
print(f"Genre: {music_genre}")
print(f"Vibe: {vibe}")
print(f"Song suggestions: {songs_sugestions}")