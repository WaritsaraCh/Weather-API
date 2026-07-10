# Weather API

A simple Flask-based weather API that returns current weather information for a city using the Visual Crossing Weather API.

## Features

- Fetches current weather data for any city
- Returns temperature, conditions, humidity, wind speed, and weather icon
- Uses Redis for caching responses to improve performance
- Applies basic rate limiting to prevent excessive requests
- Supports environment-based configuration via a `.env` file

## Project Structure

- `app.py` - Main Flask application and API routes
- `requirements.txt` - Python dependencies
- `.env` - Environment variables for API key and Redis URL

## Requirements

- Python 3.10+
- Redis server (optional, but recommended for caching)
- A Visual Crossing API key

## Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following values:
   ```env
   API_KEY=your_visual_crossing_api_key
   REDIS_URL=redis://localhost:6379/0
   ```

## Run the Application

Start the Flask server:

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

## API Endpoint

### Get weather for a city

```http
GET /weather/<city>
```

Example:

```http
GET /weather/Bangkok
```

Response example:

```json
{
  "city": "Bangkok",
  "temperature": 32,
  "conditions": "Clear",
  "humidity": 62,
  "wind_speed": 10,
  "icon": "clear-day",
  "source": "3rd Party API (Visual Crossing)"
}
```

## Notes

- If Redis is not available, the app will still run using in-memory storage for rate limiting.
- The app uses a simple cache key format such as `weather:bangkok`.
- Rate limiting is set to 5 requests per minute for the weather endpoint.