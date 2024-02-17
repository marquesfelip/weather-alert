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

    def app(self) -> str | None:
        logging.basicConfig(level=logging.ERROR)

        try:
            zip_code: str = "14150-000"
            country_code: str = "BR"

            gc_city = Geocoding(zip_code, country_code).get_coordinates()

            lat = gc_city["lat"]
            lon = gc_city["lon"]

            city_weather = OpenWeatherMap(lat, lon).get_weather()

            # main = city_weather["weather"][0]["main"]
            description = city_weather["weather"][0]["description"]
            temperature = city_weather["main"]["temp"]
            feels_like = city_weather["main"]["feels_like"]
            humidity = city_weather["main"]["humidity"]

            current_time = datetime.now()
            current_time = f"{current_time.day}/{current_time.month}/{current_time.year} - {current_time.hour}:{current_time.minute}:{current_time.second}"

            if self.__weather != description:
                self.__weather = description
                print(current_time)
                print(description)
                print(temperature)
                print(feels_like)
                print(humidity)

                publisher = RabbitmqPublisher()
                publisher.send_message(
                    f"Horário: {current_time}\nClima: {description}\nTemperatura: {temperature}\nSensação Térmica: {feels_like}\nUmidade: {humidity}"
                )
            else:
                print(
                    f"Horário: {current_time}\nClima: {description}\nTemperatura: {temperature}\nSensação Térmica: {feels_like}\nUmidade: {humidity}"
                )

        except:
            logging.error(traceback.format_exc())
        finally:
            time.sleep(10)
            self.app()
