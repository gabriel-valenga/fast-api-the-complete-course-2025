from fastapi import FastAPI, Body

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
async def return_books_by_author_filtering_by_category(author:str, category:str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get('author').casefold() == author.casefold() 
            and book.get('category').casefold() == category.casefold() 
        ):
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
            