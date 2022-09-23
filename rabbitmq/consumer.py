import asyncio
import os

import pika
from dotenv import load_dotenv

load_dotenv(".env")


async def consume(method, callback):
    print(method)
    connection = pika.BlockingConnection(pika.URLParameters(os.environ["RABBITMQ_URL"]))
    channel = connection.channel()
    print("function called")
    channel.queue_declare(method, durable=True)
    #channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=method, on_message_callback=callback, auto_ack=True)
    await channel.start_consuming()
