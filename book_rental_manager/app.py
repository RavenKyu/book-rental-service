from functools import wraps

from flask import Flask, request, make_response
from flask_restx import Resource, Api, reqparse, abort

from sqlalchemy.orm.exc import (NoResultFound)
from werkzeug.exceptions import(BadRequest)

from book_rental_manager.database import db_session
from book_rental_manager.models import (Customer, Book, Rental)
from book_rental_manager.logger import get_logger



app = Flask(__name__)
api = Api(app)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

logger = get_logger('API')

customers_parser = reqparse.RequestParser()
customers_parser.add_argument('name', type=str, help="Cutomer's name", store_missing=False)
customers_parser.add_argument('phone', type=str, help="Customer's phone number", store_missing=False)


def result(f):
    @wraps(f)
    def func(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
        except NoResultFound as e:
            logger.exception(msg=str(e), exc_info=e)
            api.abort(404, 'There is not the index')
        except Exception as e:
            logger.exception(msg=str(e), exc_info=e)
            raise
        return result, 200
    return func

def get_column_names(model):
    columns = [str(x) for x in model.__table__.columns]
    columns = [x[x.rfind('.')+1:] for x in columns]
    return columns


@api.route('/customers')
class Customers(Resource):
    @result
    def get(self):
        args = customers_parser.parse_args()
        query = Customer.query
        columns = get_column_names(Customer)
        target = set(columns) & set(list(args.keys()))
        for t in list(target):
            customer = getattr(Customer, t)
            query = query.filter(customer.like(f'%{args[t]}%'))
        customer = query.all()
        # customer = Customer.query.filter_by(**args).all()
        return [c.as_dict() for c in customer]

    @result
    def post(self):
        request.get_json(force=True)
        args = customers_parser.parse_args()
        customer = Customer(**args)
        db_session.add(customer)
        db_session.commit()
        return None


@api.route('/customers/<int:customer_id>')
class Customers(Resource):
    def get_customer(self, customer_id):
        customer = Customer.query.filter_by(id=customer_id).one()
        return customer

    @result
    def get(self, customer_id):
        customer = self.get_customer(customer_id)
        return customer.as_dict()

    @result
    def patch(self, customer_id):
        args = customers_parser.parse_args()
        customer = self.get_customer(customer_id)
        customer.query.update(args)
        db_session.commit()
        return None

    @result
    def delete(self, customer_id):
        customer = self.get_customer(customer_id)
        db_session.delete(customer)
        db_session.commit()
        return None


book_parser = reqparse.RequestParser()
book_parser.add_argument('title', type=str, help="The title of the book", store_missing=False)
book_parser.add_argument('author', type=str, help="The author of the book", store_missing=False)
book_parser.add_argument('publisher', type=str, help="Publisher's name", store_missing=False)


@api.route('/books')
class Books(Resource):
    @result
    def get(self):
        args = book_parser.parse_args()
        query = Book.query
        columns = get_column_names(Book)
        target = set(columns) & set(list(args.keys()))
        for t in list(target):
            book = getattr(Book, t)
            query = query.filter(book.like(f'%{args[t]}%'))
        book = query.all()
        # book = book.query.filter_by(**args).all()
        return [c.as_dict() for c in book]

    @result
    def post(self):
        request.get_json(force=True)
        args = book_parser.parse_args()
        book = Book(**args)
        db_session.add(book)
        db_session.commit()
        return None