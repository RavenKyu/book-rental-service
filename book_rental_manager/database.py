import os
import time
import random
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_FILENAME = 'book_rental_manager'
engine = create_engine(f'sqlite:///{DB_FILENAME}.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    os.rename(f'{DB_FILENAME}.db', f'{DB_FILENAME}_{str(int(time.time()))}.db')
    import book_rental_manager.models
    Base.metadata.create_all(bind=engine)

def dummy_members():
    from book_rental_manager.models import CustomerFactory
    names = [CustomerFactory() for _ in range(30)]
    db_session.commit()

def dummy_books():
    from book_rental_manager.models import BookFactory
    book = [BookFactory() for _ in range(100)]
    db_session.commit()

def dummy_rental():
    from book_rental_manager.models import RentalFactory
    from book_rental_manager.models import CustomerFactory
    from book_rental_manager.models import BookFactory
    Book = BookFactory._meta.model
    Customer = CustomerFactory._meta.model
    Rental = RentalFactory._meta.model

    for _ in range(1000):
        book = random.choice(Book.query.filter(Book.rentals==None).all())
        member = random.choice(Customer.query.all())
        rental = RentalFactory()
        rental.book = book
        rental.customer = member
        if random.randrange(1, 3) % 2 == 0:
            rental.rental_end = datetime.datetime.now()
    db_session.commit()
    


    
