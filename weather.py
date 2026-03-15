#!/usr/bin/env python3
"""
Personal Weather Station Reader
Fetches current weather data, 7-day history, and forecast from TWC API.
"""

import json
import requests
import logging
from pathlib import Path
from datetime import datetime

# Setup
SCRIPT_DIR = Path(__file__).parent
SECRETS_FILE = SCRIPT_DIR / "secrets.json"
LOG_FILE = SCRIPT_DIR / "weather.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def load_secrets():
    """Load API credentials from secrets file."""
    try:
        with open(SECRETS_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Secrets file not found: {SECRETS_FILE}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in secrets file: {SECRETS_FILE}")
        return None


def fetch_current_weather(api_key, station_id):
    """Fetch current weather data from TWC API."""
    url = "https://api.weather.com/v2/pws/observations/current"
    params = {
        "stationId": station_id,
        "format": "json",
        "units": "e",
        "apiKey": api_key,
        "numericPrecision": "decimal"
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Current weather API request failed: {e}")
        return None


def fetch_7day_history(api_key, station_id):
    """Fetch 7-day history from TWC API."""
    url = "https://api.weather.com/v2/pws/dailysummary/7day"
    params = {
        "stationId": station_id,
        "format": "json",
        "units": "e",
        "apiKey": api_key,
        "numericPrecision": "decimal"
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"7-day history API request failed: {e}")
        return None


def fetch_forecast(api_key, lat, lon):
    """Fetch 5-day forecast from TWC API."""
    url = "https://api.weather.com/v3/wx/forecast/daily/5day"
    params = {
        "geocode": f"{lat},{lon}",
        "format": "json",
        "units": "e",
        "language": "en-US",
        "apiKey": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Forecast API request failed: {e}")
        return None


def format_current_weather(data):
    """Format current weather data for display."""
    if not data or "observations" not in data:
        return "No current weather data available"
    
    obs = data["observations"][0] if data["observations"] else {}
    imperial = obs.get("imperial", {})
    
    lines = [
        "🌤️  CURRENT CONDITIONS:",
        f"   Temperature:    {imperial.get('temp', 'N/A')}°F",
        f"   Feels Like:     {imperial.get('feelsLike', 'N/A')}°F",
        f"   Humidity:       {obs.get('humidity', 'N/A')}%",
        f"   Wind Speed:     {imperial.get('windSpeed', 'N/A')} mph",
        f"   Wind Gust:      {imperial.get('windGust', 'N/A')} mph",
        f"   Wind Direction: {obs.get('winddir', 'N/A')}°",
        f"   Dew Point:      {imperial.get('dewpt', 'N/A')}°F",
        f"   UV Index:       {obs.get('uv', 'N/A')}",
    ]
    
    return "\n".join(lines)


def format_7day_history(data):
    """Format 7-day history data for display."""
    if not data or "summaries" not in data:
        return "No 7-day history available"
    
    summaries = data["summaries"]
    if not summaries:
        return "No 7-day history available"
    
    lines = ["", "📅 7-DAY HISTORY:"]
    
    for i, day in enumerate(summaries):
        imperial = day.get("imperial", {})
        date_str = day.get("obsTimeLocal", "N/A").split()[0]
        
        temp_high = imperial.get("tempHigh", "N/A")
        temp_low = imperial.get("tempLow", "N/A")
        precip = imperial.get("precipTotal", 0)
        humidity_avg = day.get("humidityAvg", "N/A")
        wind_avg = imperial.get("windspeedAvg", "N/A")
        
        precip_str = f" 🌧️{precip}\"" if precip and precip > 0 else ""
        lines.append(f"   {date_str}: {temp_low}°-{temp_high}°F | Humidity: {humidity_avg}% | Wind: {wind_avg} mph{precip_str}")
    
    return "\n".join(lines)


def format_forecast(data):
    """Format forecast data for display."""
    if not data:
        return ""
    
    if "dayOfWeek" not in data:
        return ""
    
    days_of_week = data.get("dayOfWeek", [])
    temps_max = data.get("temperatureMax", [])
    temps_min = data.get("temperatureMin", [])
    narratives = data.get("narrative", [])
    
    if not days_of_week:
        return ""
    
    lines = ["", "🔮 5-DAY FORECAST:"]
    
    for i in range(min(5, len(days_of_week))):
        day_name = days_of_week[i]
        temp_max = temps_max[i] if i < len(temps_max) and temps_max[i] is not None else "N/A"
        temp_min = temps_min[i] if i < len(temps_min) and temps_min[i] is not None else "N/A"
        narrative = narratives[i] if i < len(narratives) else "No description"
        
        # Clean up narrative - take first sentence or first 60 chars
        if narrative:
            narrative = narrative.split('.')[0][:60]
        
        lines.append(f"   {day_name}: {temp_min}°-{temp_max}°F - {narrative}")
    
    return "\n".join(lines)


def main():
    """Main entry point."""
    secrets = load_secrets()
    if not secrets:
        print("❌ Failed to load API credentials")
        return
    
    api_key = secrets["api_key"]
    station_id = secrets["station_id"]
    
    # Fetch current weather
    current_data = fetch_current_weather(api_key, station_id)
    if not current_data:
        print("❌ Failed to fetch current weather data")
        return
    
    # Extract coordinates for forecast
    obs = current_data.get("observations", [{}])[0]
    lat = obs.get("lat")
    lon = obs.get("lon")
    
    # Fetch 7-day history
    history_data = fetch_7day_history(api_key, station_id)
    if not history_data:
        print("❌ Failed to fetch 7-day history data")
        return
    
    # Fetch forecast
    forecast_data = None
    if lat and lon:
        forecast_data = fetch_forecast(api_key, lat, lon)
    
    # Format and display
    current_output = format_current_weather(current_data)
    history_output = format_7day_history(history_data)
    forecast_output = format_forecast(forecast_data) if forecast_data else ""
    
    print(current_output)
    print(history_output)
    if forecast_output:
        print(forecast_output)
    print()
    logging.info("Current weather, 7-day history, and forecast retrieved successfully")


if __name__ == "__main__":
    main()
