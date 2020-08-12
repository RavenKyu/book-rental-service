from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

__all__  = (
    'Customer',
    'Book',
    'Rental'
)

from sqlalchemy.ext.declarative import declarative_base
BaseModel = declarative_base()


class Customer(BaseModel):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    customer_phone = Column(String)

    def __init__(self, customer_name, customer_phone):
        self.customer_name = customer_name
        self.customer_phone = customer_phone

    def __repr__(self):
        return f"<User('{self.customer_name}', '{self.customer_phone}')>" 


class Book(BaseModel):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True)
    book_title = Column(String)
    book_author = Column(String)
    book_isbn = Column(String)

    def __init__(self, book_title, book_author, book_isbn):
        self.book_title = book_title
        self.book_author = book_author
        self.book_isbn = book_isbn

    def __repr__(self):
        return f"<Book('{self.book_title}', '{self.book_author}', '{self.book_isbn}')>" 


class Rental(BaseModel):
    __tablename__ = 'rental'

    book_id = Column(Integer, ForeignKey(Book.book_id), primary_key=True)
    customer_id = Column(Integer, ForeignKey(Customer.customer_id), primary_key=True)
    rental_start = Column(Integer)
    rental_end = Column(Integer)

    # book = relationship("Book", backref=backref('rental', order_by=book_id))
    # customer = relationship("Customer", backref=backref('rental', order_by=customer_id))

    def __init__(self, rental_start:int):
        self.rental_start = rental_start
    
    def __repr__(self):
        return f"<Rental('{self.rental_start}', '{self.rental_end}')>" 


