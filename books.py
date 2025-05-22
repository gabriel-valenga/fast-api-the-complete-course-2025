from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},    
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'}
]

@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_book_filter_by_book_title(book_title):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return {'message': f'not found a book with title: {book_title}'}


@app.get("/books/mybook")
async def read_my_favorite_book():
    return {'book title': 'My Favorite Book'}