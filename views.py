#!venv/bin/python
import json
import uuid

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from rabbitmq.consumer import consume
from rabbitmq.producer import Publish

load_dotenv(".env")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/add-book/")
async def add_book(request: Request):
    book = await request.json()
    rid = Publish("logs").call(book)
    return rid

@app.post("/add-author/")
async def add_author(request: Request):
    author = await request.json()
    rid = Publish("logs").call(author)
    return rid

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
