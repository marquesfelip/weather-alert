from dotenv import load_dotenv
import requests
import os
import logging
import traceback


class Geocoding:
    load_dotenv()
    logging.basicConfig(level=logging.ERROR)

    def __init__(self, zip_code: str, country_code: str):
        self.__zip_code = zip_code
        self.__country_code = country_code
        self.__API_TOKEN = os.getenv("OPENWEATHER_API_TOKEN")

    def get_coordinates(self) -> dict:
        """Retorna as coordenadas da cidade"""

        try:
            url = f"https://api.openweathermap.org/geo/1.0/zip?zip={self.__zip_code},{self.__country_code}&appid={self.__API_TOKEN}"
            response = requests.get(url=url, timeout=None)

            if response.status_code != 200:
                print(f"Erro na requisição.\nStatus: {response.status_code}")
                return f"Erro na requisição.\nStatus: {response.status_code}"
        except:
            logging.error(traceback.format_exc())
        finally:
            return response.json()
