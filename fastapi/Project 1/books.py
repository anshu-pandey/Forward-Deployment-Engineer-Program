from fastapi import Body,FastAPI, HTTPException
BOOKS = [
    {"title": "Title 1", "author": "Author 1", "category": "Science"},
    {"title": "Title 2", "author": "Author 2", "category": "History"},
    {"title": "Title 3", "author": "Author 3", "category": "Math"},
    {"title": "Title 4", "author": "Author 4", "category": "Science"},
    {"title": "Title 5", "author": "Author 5", "category": "History"}
]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello in World of books ..."}

# GET: Read all books ( Static API endpoint )
@app.get("/books")
async def read_all_books():
    return BOOKS


## Static API always should be defined before dynamic API endpoints.
##  Otherwise, the static API will never be reached.
@app.get("/books/mybook")
async def read_favorite_book():
    return {"book_title": "My Favorite Book"}


# GET: Read a specific book by title {Query Parameter}  ( Dynamic API endpoint )
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
    '''Note: Returning an error dictionary above produces a normal successful HTTP 
    response unless you explicitly set an error status. 
    A more appropriate implementation uses HTTPException(status_code=404).'''

    raise HTTPException(
    status_code=404,
    detail="Book not found"
    )