#!venv/bin/python
import json
import uuid

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from rabbitmq.consumer import consume
from rabbitmq.producer import publish

load_dotenv(".env")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/add-book/")
async def add_book(request: Request):
    book = await request.json()
    uid ={"taskId":str(uuid.uuid4())}
    book.update(uid)
    publish("logs",book)
    return uid



def callback(ch, method, properties, body):
    print(body)
    gi = json.loads(body)
    print(body)
    print(gi)
    return gi

@app.post("/add-author/")
async def add_author(request: Request):
    author = await request.json()
    gid = str(uuid.uuid4())
    uid ={"taskId":gid}
    author.update(uid)
    publish("logs",author)
    return uid

@app.get("/get-status/{item_id}")
async def get_status(item_id):
    print(item_id)
    gi = await consume("item_id",callback)
    return gi

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
