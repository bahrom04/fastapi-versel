import requests
from fastapi import FastAPI, HTTPException


app = FastAPI()

API_KEY = "00de3e3400f5ef50f02428295585eba5"


@app.get("/{city_name}")
def root(city_name: str):
    try:
        response = requests.get(
          f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
        )
    except:
        raise HTTPException(status_code=400, detail="Email already registered")

    return {"data": response.json()}