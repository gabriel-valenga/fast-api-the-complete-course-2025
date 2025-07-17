from fastapi import FastAPI, HTTPException, Response, status
from book_request_model import CreateBookRequestModel, UpdateBookRequestModel
from library import Library

app = FastAPI()
library = Library()

@app.get("/books")
def return_all_books():
    return library.get_all_books()


@app.get("/book/id")
def get_book_by_id(id: int):
    try:
        book = library.get_book_by_id(id)
        return book
    except HTTPException as e:
        return Response(status_code=e.status_code, content={"message": e.detail})
    

@app.get("/books/rating")
def return_all_books_by_rating(rating: int):
    try:
        books = library.get_books_by_rating(rating)
        return books
    except HTTPException as e:
        return Response(status_code=e.status_code, content={"message": e.detail})


@app.get("/books/published-year")
def return_all_books_by_published_year(published_year: int):
    return library.get_books_by_published_year(published_year) 


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
def create_book(book_request:CreateBookRequestModel):
    return library.create_and_add_book(book_request)
    

@app.put("/update-book/{book_id}")
def update_book(book_id: int, book_request: UpdateBookRequestModel):
    return library.update_book(book_id, book_request)
    

@app.delete("/delete-book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    return library.delete_book(book_id)
    