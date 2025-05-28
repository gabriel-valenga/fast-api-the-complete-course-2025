from fastapi import Body, FastAPI
from book import Book
from book_request_model import BookRequestModel

app = FastAPI()
BOOKS = [
    Book(
        id=1, 
        title='Computer Science Pro', 
        author='codingwithroby', 
        description='A very nice book!', 
        rating=5
    ),
    Book(
        id=2, 
        title='Be Fast With FastAPI', 
        author='codingwithroby', 
        description='A great book!', 
        rating=4
    ),
    Book(
        id=3, 
        title='Master Endpoints', 
        author='codingwithroby', 
        description='An awesome book!', 
        rating=5
    ),
    Book(
        id=4, 
        title='HP1', 
        author='Author One', 
        description='Book description', 
        rating=3
    ),
    Book(
        id=5, 
        title='HP2', 
        author='Author Two', 
        description='Book description', 
        rating=2
    ),
    Book(
        id=6, 
        title='HP3', 
        author='Author Three', 
        description='Book description', 
        rating=1
    )
]

@app.get("/books")
def return_all_books():
    return BOOKS


@app.post("/create-book")
def create_book(book_request:BookRequestModel):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)
    return new_book