from dotenv import load_dotenv
import os
import pika
import json


class RabbitmqPublisher:
    load_dotenv()

    def __init__(self) -> None:
        self.__host = os.getenv("RABBITMQ_HOST")
        self.__port = os.getenv("RABBITMQ_PORT")
        self.__vhost = os.getenv("RABBITMQ_VHOST")
        self.__username = os.getenv("RABBITMQ_USER")
        self.__password = os.getenv("RABBITMQ_PASS")
        self.__exchange = os.getenv("RABBITMQ_EXCHANGE")
        self.__routing_key = os.getenv("RABBITMQ_ROUTING_KEY")
        self.__channel = self.__create_channel()

    def __create_channel(self) -> pika.BlockingConnection:
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            virtual_host=self.__vhost,
            credentials=pika.PlainCredentials(
                username=self.__username, password=self.__password
            ),
        )

        channel = pika.BlockingConnection(connection_parameters).channel()

        return channel

    def send_message(self, body: dict | str):
        self.__channel.basic_publish(
            exchange=self.__exchange,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(content_encoding="utf-8", delivery_mode=2),
        )
