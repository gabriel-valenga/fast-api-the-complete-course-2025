from fastapi import FastAPI, HTTPException, Response
from book_request_model import CreateBookRequestModel, UpdateBookRequestModel
from library import Library

app = FastAPI()
library = Library()

@app.get("/books")
def return_all_books():
    return library.get_all_books()


@app.get("/book/id")
def get_book_by_id(id: int):
    book = library.get_book_by_id(id)
    if book:
        return book
    else:
        return Response(status_code=404, content={"message": "Book not found"})
    

@app.get("/books/rating")
def return_all_books_by_rating(rating: int):
    books = library.get_books_by_rating(rating)
    if books:
        return books
    else:
        return Response(status_code=404, content={"message": "No books found with the given rating"})


@app.post("/create-book")
def create_book(book_request:CreateBookRequestModel):
    new_book = library.create_and_add_book(book_request)
    return new_book
    

@app.put("/update-book/{book_id}")
def update_book(book_id: int, book_request: UpdateBookRequestModel):
    try:
        updated_book = library.update_book(book_id, book_request)
        return updated_book
    except HTTPException as e:
        return Response(status_code=e.status_code, content={"message": e.detail})
    

@app.delete("/delete-book/{book_id}")
def delete_book(book_id: int):
    try:
        return library.delete_book(book_id)
    except HTTPException as e:
        return Response(status_code=e.status_code, content={"message": e.detail})