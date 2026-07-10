import json

from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import redis

load_dotenv()

app = Flask(__name__)

WEATHER_API_KEY = os.getenv("API_KEY")
REDIS_URL = os.getenv("REDIS_URL")

try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
except Exception as e:
    print(f'Error connecting to Redis: {e}')
    redis_client = None

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    if not WEATHER_API_KEY:
        return jsonify({"error": "Weather API key is not set."}), 500
    
    cache_key = f"weather:{city.lower()}"
    if redis_client:
        cached_weather = redis_client.get(cache_key)
        if cached_weather:
            weather_data = json.loads(cached_weather)
            weather_data["source"] = "Redis Cache 🚀 (Super Fast!)" 
            return jsonify(weather_data), 200
        
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({'error': f'Failed to fetch weather data for {city}. Status code: {response.status_code}'}), response.status_code
        
        data = response.json()
        result = {
            "city": city,
            "temperature": data.get("currentConditions", {}).get("temp"),
            "conditions": data.get("currentConditions", {}).get("conditions"),
            "humidity": data.get("currentConditions", {}).get("humidity"),
            "wind_speed": data.get("currentConditions", {}).get("windspeed"),
            "icon": data.get("currentConditions", {}).get("icon"),
            "source": "3rd Party API (Visual Crossing)"
        }
        if redis_client:
            redis_client.setex(cache_key, 3600, json.dumps(result))
        
        return jsonify(result), 200
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)