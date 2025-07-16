class Book:
    id: int
    title: str 
    author: str
    description: str
    rating: int
    published_year: int


    def __init__(
        self,
        id: int,
        title: str = None,
        author: str = None,
        description: str = None, 
        rating:str = None,
        published_year: int = None 
    ):
        self.id = id 
        self.title = title 
        self.author = author 
        self.description = description 
        self.rating = rating
        self.published_year = published_year
