import time
import factory
import datetime
from sqlalchemy import Column, Integer, String, Unicode, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from book_rental_manager.database import Base, db_session


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
        return f"<Customer('{self.name}', {self.phone})>" 

class CustomerFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Customer
        sqlalchemy_session = db_session
        sqlalchemy_get_or_create = ('name', 'phone')

    name = factory.Faker('name', locale='ko_KR')
    phone = factory.Faker('phone_number', locale='ko_KR')


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

class BookFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Book
        sqlalchemy_session = db_session
        sqlalchemy_get_or_create = ('title', 'author', 'publisher')

    title = factory.Faker('catch_phrase', locale='ko_KR')
    author = factory.Faker('name', locale='ko_KR')
    publisher = factory.Faker('company', locale='ko_KR')

class Rental(Base):
    __tablename__ = 'rental'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id))
    customer_id = Column(Integer, ForeignKey(Customer.id))
    rental_start = Column(DateTime)
    rental_end = Column(DateTime, default=datetime.datetime.fromtimestamp(0))

    book = relationship("Book", 
        backref=backref("rentals", cascade="all, delete, delete-orphan", foreign_keys='Rental.book_id'))
    customer = relationship("Customer", 
        backref=backref("rentals", cascade="all, delete, delete-orphan", foreign_keys='Rental.customer_id'))
    # customer = relationship("Customer", backref=backref('rentals')) 

    def __init__(self, rental_start=0):
        self.rental_start = rental_start

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def __repr__(self):
        return f"<Rental({self.customer}, {self.book}, '{self.rental_start}', '{self.rental_end}')>" 

class RentalFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Rental
        sqlalchemy_session = db_session
        sqlalchemy_get_or_create = ('rental_start',)

    rental_start = factory.Faker('date_time_between', locale='ko_KR', start_date='-3d', end_date='now')

