import asyncio
import json
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Author as ModelAuthor
from models import Book as ModelBook
from rabbitmq.consumer import consume, send_back

load_dotenv(".env")
engine = create_engine(os.environ['DATABASE_URL'])

def add_author(author):
    db_author = ModelAuthor(name=author["name"], age=author["age"])
    with Session(bind=engine) as d:
        d.add(db_author)
        d.commit()
        id = {"recordId":db_author.id}
    return id

def add_book(book):
    db_book = ModelBook(title=book["title"], rating=book["rating"], author_id=book["author_id"])
    with Session(bind=engine) as d:
        d.add(db_book)
        d.commit()
        id = {"recordId":db_book.id}
    return id

def callback(ch, method, properties, body):
    body = json.loads(body)
    if "author" in body:
        id = add_author(body["author"])
    elif "book" in body:
        id = add_book(body["book"])
    send_back(ch, method, properties, id)

async def consumer():
    await consume("logs",callback)

if __name__ == "__main__":
    asyncio.run(consumer())
