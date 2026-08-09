# Weather Mood Music

A command-line Python program that combines real-time weather data with AI to suggest a music genre, vibe, and song recommendations tailored to how you're feeling and the weather outside. Built to practice working with multiple external APIs, environment variable security, and AI prompt engineering.

## How it works

1. You enter your zip code and describe your current mood
2. The program calls the OpenWeatherMap API to pull real-time weather conditions and temperature for your location
3. That weather data, combined with your mood, is sent to the Claude API (Anthropic) with a prompt engineered to return structured JSON
4. The AI's response is parsed and displayed as a suggested music genre, a vibe description, and three song suggestions

## Features

- **Real-time weather integration**: pulls live conditions (temperature, general weather category) via the OpenWeatherMap API based on user-provided zip code
- **AI-powered recommendations**: uses the Claude API to reason over weather + mood and generate a tailored music suggestion
- **Reliable structured output**: prompt is engineered to request an exact JSON structure with fixed keys, so output is consistent and parseable every run
- **Secure API key management**: all API keys are stored in a `.env` file (excluded from version control via `.gitignore`) and loaded at runtime, never hardcoded
- **Clean JSON parsing**: strips markdown formatting from the AI's response and converts it into a Python dictionary for easy access

## How to run it

```bash
python weather_mood_music.py
```

You'll be prompted for your zip code and your current mood — the program will then print your suggested genre, vibe description, and three song recommendations.

## Setup

This project requires your own API keys, which are not included in this repo:

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Get an API key from the [Anthropic Console](https://console.anthropic.com)
3. Create a `.env` file in the project root with:
```
OPEN_WEATHER_API_KEY="your_key_here"
ANTHROPIC_API_KEY="your_key_here"
```
4. Install dependencies: `pip install python-dotenv requests anthropic`

## Planned next steps

- **Spotify integration**: querying the Spotify API to pull real preview clips for each AI-suggested song, so users can actually listen to a short sample rather than just seeing text suggestions. This will require setting up OAuth authentication with Spotify's API.

## Notes

- Weather lookups are currently limited to U.S. zip codes
- Extended thinking is disabled on the AI call since this task doesn't require deep reasoning, keeping responses fast and token-efficient