import asyncio
import json
import os

import pika
from dotenv import load_dotenv

load_dotenv(".env")


async def consume(method, callback):
    connection = pika.BlockingConnection(pika.URLParameters(os.environ["RABBITMQ_URL"]))
    channel = connection.channel()
    print("function called")
    channel.queue_declare(method, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=method, on_message_callback=callback)
    await channel.start_consuming()

def send_back(ch, method, props, response):
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
