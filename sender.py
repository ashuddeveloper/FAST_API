
import os
import sys

import pika
from dotenv import load_dotenv

load_dotenv(".env")
connection = pika.BlockingConnection(pika.URLParameters(os.environ["RABBITMQ_URL"]))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()
