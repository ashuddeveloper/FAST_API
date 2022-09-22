
import json
import os

import pika
from dotenv import load_dotenv

load_dotenv(".env")
connection = pika.BlockingConnection(pika.URLParameters(os.environ["RABBITMQ_URL"]))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(body),properties=properties)
