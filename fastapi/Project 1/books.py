from fastapi import Body,FastAPI, HTTPException
from typing import Optional

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


# GET: Read a specific book by title {Path Parameter}  ( Dynamic API endpoint )
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



## Query Parameter: Read books by category 
'''Important: FastAPI automatically identifies category as a query parameter 
because it is not declared as a path parameter and is a simple type (str).'''
@app.get("/v2/books")
def read_category_by_query(category: str):
    books_to_return = []

    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


## Query Parameter with Path Parameter: Read books by author and category
"""FastAPI automatically assigns the values based on their names and locations.
book_author receives its value from the URL path.
category receives its value from the query string.
"""

@app.get("/v2/books/{book_author}")
def read_author_category(
    book_author: str,
    category: str
):
    books_to_return = []

    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)

    return books_to_return


##How to make the query parameter optional?

@app.get("/v2/qp/books/{book_author}")
def read_author_category(
    book_author: str,
    category: Optional[str] = None
):
    books_to_return = []

    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold():

            if category is None or book.get("category").casefold() == category.casefold():
                books_to_return.append(book)

    return books_to_return



'''Important: The new_book variable
 receives whatever data the client sends in the request body.'''
@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

# PUT: Update a book by title
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            break

## Delete without body ( This is the recommended way to delete a resource )
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

## If delete have a body 
@app.delete("/books/delete_book_with_body")
async def delete_book(book_title=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


## What happen if we want to read a book by title but the title is sent in the request body instead of path parameter?
@app.get("/bookstitle_with_body")
async def read_book(book_title =Body()):
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
