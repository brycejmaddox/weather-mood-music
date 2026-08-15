# Weather Mood Music

A command-line Python program that combines real-time weather data with AI to suggest a music genre, vibe, and song recommendations tailored to how you're feeling and the weather outside — complete with links to listen on Spotify. Built to practice working with multiple external APIs, OAuth authentication, environment variable security, and AI prompt engineering.

## How it works

1. You enter your zip code and describe your current mood
2. The program calls the OpenWeatherMap API to pull real-time weather conditions and temperature for your location
3. That weather data, combined with your mood, is sent to the Claude API (Anthropic) with a prompt engineered to return structured JSON
4. The AI's response is parsed into a suggested music genre, a vibe description, and three song suggestions
5. Each suggested song is searched on Spotify via the Web API, and a direct link to the track is returned
6. The program prints your genre, vibe, and each song alongside a clickable Spotify link

## Features

- **Real-time weather integration**: pulls live conditions (temperature, general weather category) via the OpenWeatherMap API based on user-provided zip code
- **AI-powered recommendations**: uses the Claude API to reason over weather + mood and generate a tailored music suggestion
- **Reliable structured output**: prompt is engineered to request an exact JSON structure with fixed keys, so output is consistent and parseable every run
- **Spotify integration with OAuth**: authenticates with Spotify's API using the Client Credentials flow (Base64-encoded credential exchange for a temporary access token), then searches for each AI-suggested song to return a direct listening link
- **Secure API key management**: all API keys are stored in a `.env` file (excluded from version control via `.gitignore`) and loaded at runtime, never hardcoded
- **Clean JSON parsing**: strips markdown formatting from the AI's response and navigates nested JSON structures (weather data, AI output, and Spotify search results) to extract exactly what's needed

## How to run it

```bash
python weather_mood_music.py
```

You'll be prompted for your zip code and your current mood — the program will then print your suggested genre, vibe description, and three song recommendations, each with a link to the track on Spotify.

## Setup

This project requires your own API keys, which are not included in this repo:

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Get an API key from the [Anthropic Console](https://console.anthropic.com)
3. Create an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) to get a Client ID and Client Secret
4. Create a `.env` file in the project root with:
```
OPEN_WEATHER_API_KEY="your_key_here"
ANTHROPIC_API_KEY="your_key_here"
SPOTIFY_CLIENT_ID="your_client_id_here"
SPOTIFY_CLIENT_SECRET="your_client_secret_here"
```
5. Install dependencies: `pip install python-dotenv requests anthropic`

## Notes

- Weather lookups are currently limited to U.S. zip codes
- Extended thinking is disabled on the AI call since this task doesn't require deep reasoning, keeping responses fast and token-efficient
- Spotify deprecated the `preview_url` field (a direct link to a short audio clip) for new apps in late 2024, so this project links to each track's Spotify page instead, where users can listen via the Spotify app or web player