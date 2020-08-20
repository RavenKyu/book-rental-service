import os
import time
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
