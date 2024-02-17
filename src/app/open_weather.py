from dotenv import load_dotenv
import requests
import os
import logging
import traceback


class OpenWeatherMap:
    load_dotenv()
    logging.basicConfig(level=logging.ERROR)

    def __init__(self, lat: str, lon: str):
        self.__lat = lat
        self.__lon = lon
        self.__API_TOKEN = os.getenv("OPENWEATHER_API_TOKEN")

    def get_weather(self) -> dict:
        """Retorna as condições climaticas da cidade"""

        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.__lat}&lon={self.__lon}&units=metric&appid={self.__API_TOKEN}"
            response = requests.get(url=url, timeout=None)

            if response.status_code != 200:
                print(f"Erro na requisição.\nStatus: {response.status_code}")
                return f"Erro na requisição.\nStatus: {response.status_code}"
        except:
            logging.error(traceback.format_exc())
        finally:
            return response.json()
