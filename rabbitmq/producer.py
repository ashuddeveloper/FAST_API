import json
import os

import pika
from dotenv import load_dotenv

load_dotenv(".env")

connection = pika.BlockingConnection(pika.URLParameters(os.environ["RABBITMQ_URL"]))
channel = connection.channel()

def publish(method, body):
    channel.queue_declare(method, durable=True)
    channel.basic_publish(
    exchange='',
    routing_key=method,
    body=json.dumps(body))
        
