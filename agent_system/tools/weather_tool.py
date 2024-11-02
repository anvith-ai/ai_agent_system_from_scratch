import requests
from agent_system.core.base_tool import BaseTool

class WeatherTool(BaseTool):
    """Tool for fetching weather information from OpenWeatherMap API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def name(self) -> str:
        return "Weather Tool"
    
    def description(self) -> str:
        return "Provides current weather information for a given location"
    
    def use(self, *args, **kwargs) -> str:
        if not args:
            return "Error: Location is required"
            
        location = args[0].split("weather in ")[-1]
        
        try:
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"]
                return f"The weather in {location} is currently {description} with a temperature of {temp}°C."
            else:
                return f"Error: {data.get('message', 'Unknown error occurred')}"
                
        except Exception as e:
            return f"Error fetching weather data: {str(e)}"