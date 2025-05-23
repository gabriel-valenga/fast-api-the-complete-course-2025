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
async def return_all_books():
    return BOOKS


@app.get("/books/{title}")
async def return_a_book_filtering_by_book_title(title:str):
    for book in BOOKS:
        if book.get('title').casefold() == title.casefold():
            return book
    return {'message': f'not found a book with title: {title}'}


@app.get("/books/mybook")
async def return_my_favorite_book():
    return {'book title': 'My Favorite Book'}


@app.get("/books/category/")
async def return_books_by_category(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/author/")
async def return_books_by_author(author:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{author}/")
async def return_books_by_author_filtering_by_category(author:str, category):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get('author').casefold() == author.casefold() 
            and book.get('category').casefold() == category.casefold() 
        ):
            books_to_return.append(book)
    return books_to_return