# main.py
from fastapi import FastAPI, HTTPException
import sqlite3
import requests
from datetime import datetime

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Ensure database table exists
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
        city TEXT PRIMARY KEY,
        pressure INTEGER,
        current_time TEXT
    )''')
    conn.commit()
    conn.close()

@app.get("/")
async def get_weather():
    # Fetch weather data from OpenWeatherMap API for Warrington
    api_key = "00de3e3400f5ef50f02428295585eba5"
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Warrington&appid={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="City not found")
    weather_data = response.json()

    # Extract pressure data
    pressure = weather_data.get('main', {}).get('pressure')
    if pressure is None:
        raise HTTPException(status_code=500, detail="Pressure data not found")

    # Store pressure data along with current time in SQLite database
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO weather (city, pressure, current_time) VALUES (?, ?, ?)",
                   ('Warrington', pressure, current_time))
    conn.commit()
    conn.close()

    return {"message": "Pressure data for Warrington stored successfully"}

@app.get("/2426803/api")
async def get_weather_for_warrington():
    # Fetch pressure data and current time from SQLite database for Warrington
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    cursor.execute("SELECT pressure, current_time FROM weather WHERE city=?", ('Warrington',))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Pressure data for Warrington not found")

    pressure, current_time = row
    return {"pressure": pressure, "current_time": current_time}
