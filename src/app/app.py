import logging
import traceback
import time
from datetime import datetime
from .geocoding import Geocoding
from .open_weather import OpenWeatherMap
from ..rabbitmq import RabbitmqPublisher


class App:
    def __init__(self):
        self.__weather = ""

    def get_current_time(self):
        return f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year} - {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"

    def fetch_and_publish_weather(self, zip_code, country_code):
        logging.basicConfig(level=logging.ERROR)

        try:
            gc_city = Geocoding(zip_code, country_code).get_coordinates()

            city_weather = OpenWeatherMap(gc_city["lat"], gc_city["lon"]).get_weather()

            description = city_weather["weather"][0]["description"]
            temperature = city_weather["main"]["temp"]
            feels_like = city_weather["main"]["feels_like"]
            humidity = city_weather["main"]["humidity"]

            current_time = self.get_current_time()
            message_to_publish = f"Time: {current_time}\nWheater: {description}\nTemperature: {temperature}\nFeels Like: {feels_like}\nHumidity: {humidity}"

            # if self.__weather != description:
            if description:
                self.__weather = description

                publisher = RabbitmqPublisher()
                publisher.send_message(message_to_publish)

        except:
            logging.error(traceback.format_exc())
        finally:
            time.sleep(60)
            self.fetch_and_publish_weather(zip_code, country_code)
