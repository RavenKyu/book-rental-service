import datetime
from functools import wraps

from flask import Flask, request, make_response, jsonify
from flask_restx import Resource, Api, reqparse, abort, fields

from sqlalchemy import inspect
from sqlalchemy.orm.exc import (NoResultFound)
from werkzeug.exceptions import(BadRequest)

from book_rental_manager.database import db_session, s_session
from book_rental_manager.models import (Customer, Book, Rental)
from book_rental_manager.logger import get_logger



app = Flask(__name__)
api = Api(app)

@app.teardown_request
def shutdown_session(exception=None):
    s_session.remove()

logger = get_logger('API')

customers_parser = reqparse.RequestParser()
customers_parser.add_argument('name', type=str, help="Cutomer's name", store_missing=False)
customers_parser.add_argument('phone', type=str, help="Customer's phone number", store_missing=False)


def result(f):
    @wraps(f)
    def func(*args, **kwargs):
        try:
            r = f(*args, **kwargs)
            return jsonify(r)
            # return make_response(jsonify(result), 200)
        except NoResultFound as e:
            logger.exception(msg=str(e), exc_info=e)
            api.abort(404, 'There is not the index')
        except Exception as e:
            logger.exception(msg=str(e), exc_info=e)
            raise
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


@api.route('/books/<int:book_id>')
class Books(Resource):
    def get_a_book(self, book_id):
        book = Book.query.filter_by(id=book_id).one()
        return book

    @result
    def get(self, book_id):
        book = self.get_a_book(book_id)
        return book.as_dict()

    @result
    def patch(self, book_id):
        args = book_parser.parse_args()
        book = self.get_a_book(book_id)
        book.query.update(args)
        db_session.commit()
        return None

    @result
    def delete(self, book_id):
        book = self.get_a_book(book_id)
        db_session.delete(book)
        db_session.commit()
        return None
        

rental_parser = reqparse.RequestParser()
rental_parser.add_argument('book_id', type=int, help="The title of the book", store_missing=False)
rental_parser.add_argument('customer_id', type=int, help="The author of the book", store_missing=False)
rental_parser.add_argument('rental_start', type=str, help="Publisher's name", store_missing=False)
rental_parser.add_argument('rental_end', type=str, help="Publisher's name", store_missing=False)

class DateTimeField(fields.Raw):
    """
    데이터 직렬화
    fields.DateTime에서 datetime 객체를 제대로 파싱하지 못하여 null을
    리턴. 따로 만들어서 사용
    """
    def format(self, value):
        return value.isoformat() if isinstance(value, datetime.datetime) else None

model_rental = api.model('Rental', {
    'book_id': fields.Integer,
    'customer_id': fields.Integer,
    'rental_start': DateTimeField(attribute='rental_start'),
    'rental_end': DateTimeField(attribute='rental_end')
})

@api.route('/rentals')
class Retanls(Resource):
    @result
    @api.marshal_with(model_rental)    
    def get(self):
        args = rental_parser.parse_args()
        query = Rental.query
        columns = get_column_names(Rental)
        target = ['book_id', 'customer_id']

        for t in target:
            if not hasattr(args, t):
                continue
            query = query.filter_by(**{t:args[t]})
            del args[t]

        target = set(columns) & set(list(args.keys()))
        for t in list(target):
            model = getattr(Rental, t)
            query = query.filter(model.like(f'%{args[t]}%'))
        data = query.all()
        return data

    @result
    def post(self):
        request.get_json(force=True)
        args = rental_parser.parse_args()
        rental = Rental(**args)
        db_session.add(rental)
        db_session.commit()
        return None


@api.route('/rentals/<int:rental_id>')
class Rentals(Resource):
    def get_a_rental(self, rental_id):
        rental = Rental.query.filter_by(id=rental_id).one()
        return rental

    @result
    @api.marshal_with(model_rental)    
    def get(self, rental_id):
        rental = self.get_a_rental(rental_id)
        return rental

    @result
    def patch(self, rental_id):
        args = rental_parser.parse_args()
        rental = self.get_a_book(rental_id)
        rental.query.update(args)
        db_session.commit()
        return None

    @result
    def delete(self, rental_id):
        rental = self.get_a_book(rental_id)
        db_session.delete(rental)
        db_session.commit()
        return None