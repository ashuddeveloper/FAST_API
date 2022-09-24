
import json
import os
import uuid

import pika
from dotenv import load_dotenv

load_dotenv(".env")

# connection = pika.BlockingConnection(pika.URLParameters(os.environ["RABBITMQ_URL"]))
# channel = connection.channel()

# def publish(method, body):
#     channel.queue_declare(method, durable=True)
#     channel.basic_publish(
#     exchange='',
#     routing_key=method,
#     body=json.dumps(body))

class Publish(object):
    def __init__(self, service):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(os.environ["RABBITMQ_URL"]))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None
        self.service = service

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.service,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(body))
        self.connection.process_data_events(time_limit=None)
        return self.response
        
