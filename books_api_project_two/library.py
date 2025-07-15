from fastapi import HTTPException, Response
from book import Book
from book_request_model import CreateBookRequestModel, UpdateBookRequestModel

class Library:
    def __init__(self):
        self.books = [
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


    def create_book(self, book_request:CreateBookRequestModel):
        book_next_id = self.get_book_next_id()
        book_request = book_request.model_dump()
        book_request['id'] = book_next_id
        new_book = Book(**book_request)
        return new_book
    

    def update_book(self, book_id: int, book_request: UpdateBookRequestModel):
        book = self.get_book_by_id(book_id)
        if book:
            book_request = book_request.model_dump(exclude_unset=True)
            for key, value in book_request.items():
                setattr(book, key, value)
            return book
        else:
            raise HTTPException(status_code=404, detail="Book not found")
        

    def add_book(self, book: Book):
        self.books.append(book)


    def create_and_add_book(self, book_request: CreateBookRequestModel):    
        new_book = self.create_book(book_request)
        self.add_book(new_book)
        return new_book
    

    def delete_book(self, book_id: int):
        book = self.get_book_by_id(book_id)
        if book:
            self.books.remove(book)
            return Response(status_code=204)
        else:
            raise HTTPException(status_code=404, detail="Book not found")


    def get_all_books(self):
        return self.books
    

    def get_books_by_rating(self, rating: int):
        filtered_books = [book for book in self.books if book.rating == rating]
        if filtered_books:
            return filtered_books
        else:
            raise HTTPException(status_code=404, detail="No books found with the given rating")


    def get_book_by_id(self, book_id: int):
        for book in self.books:
            if book.id == book_id:
                return book
        raise HTTPException(status_code=404, detail="Book not found")
    

    def get_book_next_id(self):
        return 1 if len(self.books) == 0 else self.books[-1].id + 1
    