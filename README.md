# Personal Weather Station Dashboard

A Python-based weather dashboard that displays real-time weather data, historical trends, and forecasts from your personal weather station. Data is fetched from The Weather Company (TWC) API and displayed in your terminal at login.

## Purpose

This project provides a quick, convenient way to check your backyard weather conditions every time you open a terminal. Instead of visiting a web dashboard or weather app, you get a comprehensive weather overview automatically—showing current conditions, what the weather has been doing over the past week, and what to expect over the next 5 days.

## Features

### 🌤️ Current Conditions
- Real-time temperature and "feels like" temperature
- Humidity and dew point
- Wind speed, gusts, and direction
- UV index

### 📅 7-Day Historical Data
- Daily high and low temperatures
- Average humidity
- Average wind speed
- Precipitation totals (with rain emoji indicators)

### 🔮 5-Day Forecast
- Forecasted high and low temperatures
- Weather descriptions for each day
- Quick weather summary for planning

### 📝 Automatic Logging
- All weather data retrievals are logged with timestamps
- Easy tracking of when data was fetched and any errors

## Requirements

- Python 3.6+
- `requests` library
- The Weather Company (TWC) API credentials:
  - API Key
  - Personal Weather Station ID

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cecill/weather.git
cd weather
```

2. Install dependencies:
```bash
pip install requests
```

3. Create a `secrets.json` file in the project directory with your TWC API credentials:
```json
{
  "api_key": "your_api_key_here",
  "station_id": "your_station_id_here"
}
```

4. Make the script executable:
```bash
chmod +x weather.py
```

## Setup for Automatic Display at Login

Add this line to your `~/.bashrc` file to run the weather dashboard automatically every time you open a terminal:

```bash
/path/to/weather/weather.py
```

For example:
```bash
/home/username/weather/weather.py
```

Then reload your shell:
```bash
source ~/.bashrc
```

## Usage

Run the script manually:
```bash
python3 weather.py
```

Or simply open a new terminal if you've set it up in your `.bashrc`.

## API Endpoints Used

The program uses three TWC Personal Weather Station APIs:

1. **Current Observations** - Real-time weather data
   - Endpoint: `https://api.weather.com/v2/pws/observations/current`
   
2. **7-Day History** - Daily summaries for the past 7 days
   - Endpoint: `https://api.weather.com/v2/pws/dailysummary/7day`
   
3. **5-Day Forecast** - Weather forecast for the next 5 days
   - Endpoint: `https://api.weather.com/v3/wx/forecast/daily/5day`

## Output Example

```
🌤️  CURRENT CONDITIONS:
   Temperature:    35.4°F
   Feels Like:     N/A°F
   Humidity:       74.0%
   Wind Speed:     0.2 mph
   Wind Gust:      0.7 mph
   Wind Direction: 159°
   Dew Point:      28.0°F
   UV Index:       0.0

📅 7-DAY HISTORY:
   2026-03-08: 33.6°-64.0°F | Humidity: 64.7% | Wind: 5.4 mph
   2026-03-09: 45.1°-75.7°F | Humidity: 73.2% | Wind: 3.9 mph
   2026-03-10: 39.4°-65.7°F | Humidity: 98.3% | Wind: 2.1 mph 🌧️0.84"
   2026-03-11: 32.4°-49.1°F | Humidity: 94.3% | Wind: 2.0 mph 🌧️0.46"
   2026-03-12: 27.9°-48.9°F | Humidity: 67.8% | Wind: 2.1 mph
   2026-03-13: 34.9°-49.8°F | Humidity: 57.4% | Wind: 6.9 mph 🌧️0.06"
   2026-03-14: 30.9°-38.1°F | Humidity: 72.3% | Wind: 1.3 mph

🔮 5-DAY FORECAST:
   Saturday: 34°-N/A°F - Mostly cloudy
   Sunday: 24°-63°F - Windy with showers and thunderstorms
   Monday: 12°-27°F - Morning snow showers, windy
   Tuesday: 22°-28°F - Times of sun and clouds
   Wednesday: 34°-46°F - Snow showers in the morning
```

## Logging

All successful data retrievals are logged to `weather.log` in the project directory with timestamps. API errors are also logged for troubleshooting.

## Security

- Your API credentials are stored in `secrets.json`, which is excluded from version control via `.gitignore`
- Never commit `secrets.json` to a public repository
- Keep your API key private and secure

## Troubleshooting

**"Failed to load API credentials"**
- Ensure `secrets.json` exists in the project directory with valid API credentials

**"Failed to fetch weather data"**
- Check your internet connection
- Verify your API key is valid and has appropriate permissions
- Check `weather.log` for detailed error messages

**"Access Denied" for forecast**
- Your TWC subscription may not include forecast access
- The program will continue to show current conditions and history

## Files

- `weather.py` - Main Python script
- `secrets.json` - API credentials (excluded from git)
- `weather.log` - Timestamped log of all weather data retrievals
- `.gitignore` - Prevents credentials and logs from being committed

## License

This project is provided as-is for personal use.

## Getting Started with TWC API

To get your API credentials:
1. Sign up for a Weather Company Data account as a Personal Weather Station contributor
2. Create an API key in your developer dashboard
3. Note your personal weather station ID
4. Add both to `secrets.json`

For more information about the TWC APIs, see the included PDF documentation files.