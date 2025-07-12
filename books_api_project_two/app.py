from fastapi import FastAPI
from book_request_model import CreateBookRequestModel
from library import Library

app = FastAPI()
library = Library()

@app.get("/books")
def return_all_books():
    return library.get_all_books()


@app.post("/create-book")
def create_book(book_request:CreateBookRequestModel):
    new_book = library.create_and_add_book(book_request)
    return new_book


@app.get("/book/id")
def get_book_by_id(id: int):
    book = library.get_book_by_id(id)
    if book:
        return book
    else:
        return {"error": "Book not found"}
    