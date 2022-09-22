import json
import os

import pika
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import Author as ModelAuthor
from models import Book as ModelBook

load_dotenv(".env")

capp = FastAPI()

capp.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

connection = pika.BlockingConnection(pika.URLParameters(os.environ["RABBITMQ_URL"]))
channel = connection.channel()

channel.exchange_declare(exchange = 'logs', exchange_type = 'fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange = 'logs', queue=queue_name)

print(' [*] Waiting for logs to print CTRL+C')

def add_author(author):
    db_author = ModelAuthor(name=author["name"], age=author["age"])
    with db() as d:
        d.session.add(db_author)
        d.session.commit()
    return db_author

def add_book(book):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id=book.author_id)
    with db() as d:
        d.session.add(db_book)
        d.session.commit()
    return db_book

def callback(ch, method, properties, body):
    body = json.loads(body)
    if "name" in body:
        add_author(body)
    elif "book" in body:
        add_book(body)

channel.basic_consume(queue=queue_name, on_message_callback = callback, auto_ack=True)

channel.start_consuming()

if __name__ == "__main__":
    uvicorn.run(capp, host="0.0.0.0", port=4000)
