import time
from sqlalchemy import Column, Integer, String, Unicode
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from book_rental_manager.database import Base


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode)
    phone = Column(Unicode)

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"<Customer('{self.name}', '{self.phone}')>" 


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Unicode)
    author = Column(Unicode)
    publisher = Column(Unicode)

    def __init__(self, title, author, publisher):
        self.title = title
        self.author = author
        self.publisher = publisher
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"<Book('{self.title}', '{self.author}', '{self.publisher}'>" 


class Rental(Base):
    __tablename__ = 'rental'

    book_id = Column(Integer, ForeignKey(Book.id), primary_key=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), primary_key=True)
    rental_start = Column(Integer)
    rental_end = Column(Integer, default=0)

    book = relationship("Book", 
        backref=backref("rentals", cascade="all, delete, delete-orphan"))
    customer = relationship("Customer", 
        backref=backref("rentals", cascade="all, delete, delete-orphan"))
    # customer = relationship("Customer", backref=backref('rentals')) 

    def __init__(self, rental_start=None):
        if not rental_start:
            rental_start = int(time.time())
        self.rental_start = int(rental_start)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f"<Rental({self.book}, '{self.rental_start}', '{self.rental_end}')>" 


