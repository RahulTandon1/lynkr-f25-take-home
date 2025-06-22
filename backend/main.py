from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
from config import settings
from data_layer import WeatherStorage
import external_api_service

import uvicorn
    


app = FastAPI(title="Weather Data System", version="1.0.0")
weather_storage_obj = WeatherStorage()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WeatherRequest(BaseModel):
    date: str
    location: str
    notes: Optional[str] = ""

class WeatherResponse(BaseModel):
    id: str

@app.post("/weather", response_model=WeatherResponse)
async def create_weather_request(request: WeatherRequest):
    """
    You need to implement this endpoint to handle the following:
    1. Receive form data (date, location, notes)
    2. Calls WeatherStack API for the location
    3. Stores combined data with unique ID in memory
    4. Returns the ID to frontend
    """
    print(request)

    # call WeatherStack API for the location
    # response = WeatherApiService.get_weather(request.to_data_req())
    response = dict(external_api_service.WeatherApiService.get_weather(request))
    
    response["notes"] = request.notes
    # store combined data with unique ID in memory
    # response["notes"] = request.notes
    # dict(response)
    # print('available methods: ', dir(response))
    unique_id = weather_storage_obj.insert(response)
    
    # return the ID to frontend
    return WeatherResponse(id=unique_id)



from typing import Optional, List


# optional for compatibility with various types of responses
class GetWeatherResponse(BaseModel):
    class RequestInfo(BaseModel):
        type: Optional[str] = None
        query: Optional[str] = None
        language: Optional[str] = None
        unit: Optional[str] = None

    class LocationInfo(BaseModel):
        name: Optional[str] = None
        country: Optional[str] = None
        region: Optional[str] = None
        lat: Optional[str] = None
        lon: Optional[str] = None
        timezone_id: Optional[str] = None
        localtime: Optional[str] = None
        localtime_epoch: Optional[int] = None
        utc_offset: Optional[str] = None

    class AstroInfo(BaseModel):
        sunrise: Optional[str] = None
        sunset: Optional[str] = None
        moonrise: Optional[str] = None
        moonset: Optional[str] = None
        moon_phase: Optional[str] = None
        moon_illumination: Optional[int] = None

    class AirQualityInfo(BaseModel):
        co: Optional[str] = None
        no2: Optional[str] = None
        o3: Optional[str] = None
        so2: Optional[str] = None
        pm2_5: Optional[str] = None
        pm10: Optional[str] = None
        us_epa_index: Optional[str] = None
        gb_defra_index: Optional[str] = None

    class CurrentInfo(BaseModel):
        observation_time: Optional[str] = None
        temperature: Optional[int] = None
        weather_code: Optional[int] = None
        weather_icons: Optional[List[str]] = None
        weather_descriptions: Optional[List[str]] = None
        astro: Optional['GetWeatherResponse.AstroInfo'] = None
        air_quality: Optional['GetWeatherResponse.AirQualityInfo'] = None
        wind_speed: Optional[int] = None
        wind_degree: Optional[int] = None
        wind_dir: Optional[str] = None
        pressure: Optional[int] = None
        precip: Optional[int] = None
        humidity: Optional[int] = None
        cloudcover: Optional[int] = None
        feelslike: Optional[int] = None
        uv_index: Optional[int] = None
        visibility: Optional[int] = None
        is_day: Optional[str] = None

    request: Optional[RequestInfo] = None
    location: Optional[LocationInfo] = None
    current: Optional[CurrentInfo] = None
    notes: Optional[str] = ""
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Instantiate GetWeatherResponse from a dictionary (e.g., the sample response).
        """
        # Pydantic BaseModel supports .parse_obj for this purpose
        return cls.parse_obj(data)

@app.get("/weather/{weather_id}", response_model=GetWeatherResponse)
async def get_weather_data(weather_id: str):
    """
    Retrieve stored weather data by ID.
    This endpoint is already implemented for the assessment.
    """
    if not weather_storage_obj.has(weather_id):
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    return weather_storage_obj.get_by_id(weather_id)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": 200, "message": "Alive and Kicking!!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

