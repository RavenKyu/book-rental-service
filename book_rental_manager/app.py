from flask import Flask
from flask_restful import Resource, Api, reqparse
from book_rental_manager.database import db_session
from book_rental_manager.models import (Customer, Book, Rental)


app = Flask(__name__)
api = Api(app)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()



customers_parser = reqparse.RequestParser()
customers_parser.add_argument('name', type=str, help="Cutomer's name")
customers_parser.add_argument('phone', type=str, help="Customer's phone number")


class Customers(Resource):
    def get(self):
        customer = Customer.query.all()
        return str(customer)
    
    def post(self):
        args = customers_parser.parse_args()
        customer = Customer(args['name'], args['phone'])
        db_session.add(customer)
        db_session.commit()
        return 'ok'



api.add_resource(Customers, '/customers')

