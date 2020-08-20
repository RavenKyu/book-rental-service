import unittest
import pathlib
import csv
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import sqlite

from book_rental_manager.database import db_session
from book_rental_manager.models import (
    Base,
    Customer,
    Book,
    Rental,
    CustomerFactory,
    BookFactory)

CURRENT_PATH = pathlib.Path(pathlib.Path(__file__).resolve()).parent
with open(str(CURRENT_PATH / pathlib.Path('books.csv')), 'r') as f:
    reader = csv.reader(f)
    next(reader, None)
    BOOKS = list(reader)

USERS = (
    ('임덕규', '010-1234-5678'),
    ('김태진', '010-1235-5679'),
    ('박병구', '010-2236-5679'),
    ('황순용', '010-3236-5679'),
)

class DataBaseTest(unittest.TestCase):
    def setUp(self):
        self.session = db_session

    def tearDown(self):
        self.session.rollback()

    def test100_customers_tablename(self):
        self.assertEqual('customers', Customer.__tablename__)

    def test105_customers_new(self):
        c = Customer(USERS[0][0], USERS[0][1])
        self.assertEqual(USERS[0][0], c.name)
        self.assertEqual(USERS[0][1], c.phone)

    def test106_customers_filter(self):
        c = Customer(USERS[0][0], USERS[0][1])
        self.session.add(c)
        r = self.session.query(Customer)\
            .filter_by(name=USERS[0][0])\
            .first()
        self.assertEqual(USERS[0][0], r.name)
        self.assertEqual(USERS[0][1], r.phone)

    def test200_books_tablename(self):
        self.assertEqual('books', Book.__tablename__)

    def test201_books_multiple_add(self):
        for book in BOOKS:
            b = Book(*book)
            self.session.add(b)
        result = self.session.query(Book).all()
        self.assertEqual(len(result), len(BOOKS))

        result = self.session.query(Book)\
            .filter_by(author='Manuel Lima')\
            .all()
        self.assertEqual(len(result), 2)
    
    def test300_customers_as_dict(self):
        c = Customer(USERS[0][0], USERS[0][1])
        print(c.as_dict())
        self.assertTrue(False)


class QueryTest(unittest.TestCase):
    def setUp(self):
        self.session = db_session
        self.add_customers()
        self.add_books()

    def tearDown(self):
        self.session.rollback()

    def add_customers(self):
        for customer in USERS:
            self.session.add(Customer(*customer))
        self.session.commit()

    def add_books(self):
        for book in BOOKS:
            self.session.add(Book(*book))
        self.session.commit()

    def test000_check_default_data(self):
        count = self.session.query(Book).all()
        self.assertEqual(len(count), len(BOOKS))

        count = self.session.query(Customer).all()
        self.assertEqual(len(count), len(USERS))

    def test100_rental_a_book(self):
        # Customer 임덕규 객체 불러오기
        customer = self.session.query(Customer).filter_by(name='임덕규').one()
        # Book 1번 id 불러오기
        book = self.session.query(Book).filter_by(id=1).one()

        rental = Rental()
        rental.book = book
        rental.customer = customer
        self.session.add(rental)
        self.session.commit()

        r = self.session.query(Rental).one()
        self.assertEqual(r.book_id, 1)
        self.assertEqual(r.customer_id, 1)

    def test105_rental_some_books(self):
        # Customer 임덕규 객체 불러오기
        customer = self.session.query(Customer).filter_by(name='임덕규').one()
        # Book 1번 id 불러오기
        
        books = self.session.query(Book)\
            .filter(Book.id.in_([1,3,4,6]))\
            .all()
        
        for book in books:
            rental = Rental()
            rental.book = book
            rental.customer = customer
            self.session.add(rental)
        self.session.commit()

        r = self.session.query(Customer, Rental).filter(Rental.rental_end==0).filter_by(name='임덕규').all()
        self.assertEqual(r[0][0], customer)

    def test106_rental_some_books(self):
        customer = self.session.query(Customer).filter_by(name='김태진').one()
        
        books = self.session.query(Book)\
            .filter(Book.id.in_([2,5,7,8]))\
            .all()
        
        for book in books:
            rental = Rental()
            rental.book = book
            rental.customer = customer
            self.session.add(rental)
        self.session.commit()

        r = self.session.query(Rental).filter(Rental.rental_end==0).all()
        self.assertEqual(r[0].customer, customer)

    
    def test107_rental_delete_customer(self):
        """책 빌려간 사람이 삭제됐을 경우 렌트 레코드 삭제 
        """
        customer = self.session.query(Customer).filter_by(name='김태진').one()
        
        books = self.session.query(Book)\
            .filter(Book.id.in_([2,5,7,8]))\
            .all()
        
        for book in books:
            rental = Rental()
            rental.book = book
            rental.customer = customer
            self.session.add(rental)
        self.session.commit()
        r = self.session.query(Rental).filter(Rental.rental_end==0).count()
        self.assertEqual(r, 4)

        self.session.delete(customer)
        self.session.commit()
        r = self.session.query(Rental).filter(Rental.rental_end==0).count()
        self.assertEqual(r, 0)

    def test500(self):
        print(Customer.query.all())

        print(CustomerFactory(name='Raven'))
        print(Customer.query.all())
        self.assertTrue(False)

    def test600(self):
        print(BookFactory())
        self.assertTrue(False)




