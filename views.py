import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from producer import publish

load_dotenv(".env")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/add-book/")
async def add_book(request: Request):
    book = await request.json()
    publish("product_created",book)
    return book


@app.post("/add-author/")
async def add_author(request: Request):
    author = await request.json()
    publish("author_adder",author)
    return author

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
