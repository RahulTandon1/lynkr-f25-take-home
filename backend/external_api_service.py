from config import settings
from typing import Dict
from pydantic import BaseModel

import main
import requests

ACCESS_KEY = settings.WEATHER_STACK_API_KEY
 

class WeatherApiService:
    class ExternalApiRequest(BaseModel):
        date: str
        location: str

        # trying to follow Dependency inversion:
        #   Lower level constructs should depend on higher level constructs
        @classmethod
        def from_api_request(cls, arg: main.WeatherRequest):
            return cls(
                date = arg.date, 
                location = arg.location
            )
    
    @classmethod
    def _get_weather(cls, req: ExternalApiRequest) -> main.GetWeatherResponse:
        api_url =  "https://api.weatherstack.com/current"
        query_params = {
            "access_key": ACCESS_KEY,
            "query": req.location,
            "historical_date": req.date,
            "hourly": 1
        }
        response: Dict = requests.get(api_url, params=query_params).json()
        return main.GetWeatherResponse.from_dict(response)
    
    @classmethod
    def get_weather(cls, req: main.WeatherRequest) -> main.GetWeatherResponse:
        external_api_req = cls.ExternalApiRequest.from_api_request(req)
        return cls._get_weather(external_api_req)

