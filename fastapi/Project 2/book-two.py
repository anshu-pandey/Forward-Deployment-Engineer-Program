##uvicorn book-one:app --reload
## This python is only for show the purpose of creating a book class and creating a list of books.
from fastapi import Body,FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel, Field


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: int
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=5)
    rating: int = Field(gt=0, lt=6)

books = [
    Book(1, "Computer Science Pro", "Coding with Ruby",
         "A very nice book", 5),

    Book(2, "Be Fast with FastAPI", "Coding with Ruby",
         "This is a great book", 5),

    Book(3, "Master Endpoints", "Coding with Ruby",
         "This is an awesome book", 5),

    Book(4, "HP1", "Author One", "Book description", 2),

    Book(5, "HP2", "Author Two", "Book description", 3),

    Book(6, "HP3", "Author Three", "Book description", 1)
]


@app.get("/books")
async def read_all_books():
    return books


@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    books.append(new_book)
    return new_book
