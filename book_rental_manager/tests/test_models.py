import unittest

import pathlib
import csv
import time
from unittest.mock import patch
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects import sqlite

from book_rental_manager.database import db_session
from book_rental_manager.models import (
    Base,
    Customer,
    Book,
    Rental,
    CustomerFactory,
    BookFactory,
    RentalFactory)

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


class CustomerModelTest(unittest.TestCase):
    def setUp(self):
        engine = create_engine(f'sqlite:///:memory:')
        Base.metadata.create_all(bind=engine)
        session = scoped_session(
            sessionmaker(autocommit=False,
                         autoflush=False,
                         bind=engine))
        self.session = session()
        CustomerFactory._meta.sqlalchemy_session = self.session
        RentalFactory._meta.sqlalchemy_session = self.session
        BookFactory._meta.sqlalchemy_session = self.session

        self.faker = Faker()
        Faker.seed(0)

    def tearDown(self):
        self.session.rollback()
        pass

    def test100_customers_tablename(self):
        self.assertEqual('customers', Customer.__tablename__)

    def test105_customers_new(self):
        name = 'Raven'
        phone = '010-9508-0875'
        c = Customer(name, phone)
        self.assertEqual(name, c.name)
        self.assertEqual(phone, c.phone)

    def test106_customers_filter(self):
        name = 'Raven'
        phone = '010-9508-0875'
        c = Customer(name, phone)
        self.session.add(c)
        self.session.commit()
        r = self.session.query(Customer) \
            .filter_by(name=name) \
            .first()
        self.assertEqual(name, r.name)
        self.assertEqual(phone, r.phone)

    def test110_customer_factory(self):
        CustomerFactory()
        self.session.commit()
        c = self.session.query(Customer).one()
        self.assertEqual(c.name, '권영자')
        self.assertEqual(c.phone, '043-876-4759')

    def test200_books_tablename(self):
        self.assertEqual('books', Book.__tablename__)

    def test300_rental_new(self):
        rental = RentalFactory()
        self.session.commit()
        self.assertIsNone(rental.rental_end)


class QueryTest(unittest.TestCase):
    def setUp(self):
        engine = create_engine(f'sqlite:///:memory:')
        Base.metadata.create_all(bind=engine)
        session = scoped_session(
            sessionmaker(autocommit=False,
                         autoflush=False,
                         bind=engine))
        self.session = session()
        CustomerFactory._meta.sqlalchemy_session = self.session
        RentalFactory._meta.sqlalchemy_session = self.session
        BookFactory._meta.sqlalchemy_session = self.session

        self.faker = Faker()
        Faker.seed(0)

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

    def test100_rental_a_book(self):
        CustomerFactory(name='임덕규')
        BookFactory()
        self.session.commit()
        # Customer 임덕규 객체 불러오기
        customer = self.session.query(Customer).filter_by(name='임덕규').one()

        # Book 1번 id 불러오기
        book = self.session.query(Book).filter_by(id=1).one()

        rental = RentalFactory()
        rental.book = book
        rental.customer = customer
        self.session.commit()

        r = self.session.query(Rental).one()
        self.assertEqual(r.book_id, 1)
        self.assertEqual(r.customer_id, 1)

    def test105_rental_some_books(self):
        # Customer 임덕규 객체 불러오기
        CustomerFactory(name='임덕규')
        self.session.commit()
        customer = self.session.query(Customer).filter_by(name='임덕규').one()
        # Book 1번 id 불러오기
        [BookFactory() for _ in range(7)]

        self.session.commit()
        books = self.session.query(Book) \
            .filter(Book.id.in_([1, 3, 4, 6])) \
            .all()

        for book in books:
            rental = RentalFactory()
            rental.book = book
            rental.customer = customer
            self.session.add(rental)
        self.session.commit()

        r = self.session.query(Customer, Rental).filter(
            Rental.rental_end == None).filter_by(name='임덕규').all()
        self.assertEqual(4, len(r))

    def test107_rental_delete_customer(self):
        """책 빌려간 사람이 삭제됐을 경우 렌트 레코드 삭제 
        """
        CustomerFactory(name='김태진')
        [BookFactory() for _ in range(20)]
        self.session.commit()
        
        customer = self.session.query(Customer).filter_by(name='김태진').one()
        books = self.session.query(Book) \
            .filter(Book.id.in_([2, 5, 7, 8])) \
            .all()

        for book in books:
            rental = RentalFactory()
            rental.book = book
            rental.customer = customer
            self.session.add(rental)
        self.session.commit()
        r = self.session.query(Rental).filter(Rental.rental_end == None).count()
        self.assertEqual(r, 4)

        self.session.delete(customer)
        self.session.commit()
        r = self.session.query(Rental).filter(Rental.rental_end == None).count()
        self.assertEqual(r, 0)

    def test200_rental_end_datetime(self):
        b = BookFactory()
        c = CustomerFactory()
        self.session.commit()

        r = RentalFactory()
        r.book_id = b.id
        r.customer_id = c.id
        self.session.commit()

        import datetime
        r.rental_end = datetime.datetime(2020, 8, 15, 00, 00, 00)
        self.session.commit()

        self.assertIsInstance(r.rental_end, datetime.datetime)
        self.assertEqual(str(r.rental_end), '2020-08-15 00:00:00')
