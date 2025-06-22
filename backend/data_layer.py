from typing import Dict, Any, Optional
from pydantic import BaseModel



class WeatherStorage:
    def __init__(self):
        # In-memory storage for weather data
        self.store: Dict[str, Dict[str, Any]] = {}
        self.next_id = 1
    
    def get_by_id(self, id):
        return self.store.get(id)

    def has(self, id):
        return id in self.store
        
    def _get_uuid(self):
        temp_id = str(self.next_id)
        self.next_id += 1
        return temp_id

    
    # returns generated unique id
    def insert(self, data) -> str:
        id = self._get_uuid()
        self.store[ id ] = data
        return id
    







# if __name__ == '__main__':
#     sample_req = ExternalApiRequest(date='2015-01-21', location='New York', notes='')
#     print('sample req', sample_req)
#     API_URL =  "https://api.weatherstack.com/current"
#     query_params = {
#         "access_key": ACCESS_KEY,
#         "query": sample_req.location,
#         "historical_date": sample_req.date,
#         "hourly": 1
#     }
    
#     # Use HTTPS for security. Could reveal API KEY if we use HTTP
#     response = requests.get(API_URL, params=query_params).json()
#     response_obj = response
#     print('response', response_obj)
    
#     response_obj = {
#         'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'},
#         'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2025-06-22 16:59', 'localtime_epoch': 1750611540, 'utc_offset': '-4.0'},
#         'current': {
#             'observation_time': '08:59 PM', 
#             'temperature': 29, 
#             'weather_code': 200, 
#             'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0016_thundery_showers.png'], 
#             'weather_descriptions': ['Thundery outbreaks in nearby'], 
#             'astro': {'sunrise': '05:26 AM', 'sunset': '08:31 PM', 'moonrise': '02:32 AM', 'moonset': '05:53 PM', 'moon_phase': 'Waning Crescent', 'moon_illumination': 16}, 
#             'air_quality': {'co': '379.25', 'no2': '29.97', 'o3': '124', 'so2': '15.54', 'pm2_5': '28.305', 'pm10': '30.34', 'us-epa-index': '2', 'gb-defra-index': '2'}, 
#             'wind_speed': 20, 
#             'wind_degree': 240, 
#             'wind_dir': 'WSW', 
#             'pressure': 1017, 
#             'precip': 0, 
#             'humidity': 65, 
#             'cloudcover': 0, 
#             'feelslike': 30, 
#             'uv_index': 5, 
#             'visibility': 16, 
#             'is_day': 'yes'
#         }
#     }