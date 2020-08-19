from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from book_rental_manager.database import db_session
from book_rental_manager.models import (Customer, Book, Rental)


app = Flask(__name__)
api = Api(app)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()



customers_parser = reqparse.RequestParser()
customers_parser.add_argument('name', type=str, help="Cutomer's name")
customers_parser.add_argument('phone', type=int, help="Customer's phone number")


class Customers(Resource):
    def get(self):
        try:
            customer = Customer.query.all()
        except Exception as e:
            return [], 403
        return [c.as_dict() for c in customer], 200
    
    def post(self):
        request.get_json(force=True)
        args = customers_parser.parse_args()
        customer = Customer(args['name'], args['phone'])
        db_session.add(customer)
        db_session.commit()
        return 



class OneCustomer(Resource):
    def get_customer(self, customer_id):
        customer = Customer.query.filter_by(id=customer_id).all()
        if not customer:
            abort(404, message=f"The customer id {customer_id} doesn't exist.")
        return customer

    def get(self, customer_id):
        try:
            customer = self.get_customer(customer_id)
        except Exception as e:
            print(e)
            return [], 403
        return [c.as_dict() for c in customer], 200

api.add_resource(Customers, '/customers')
api.add_resource(OneCustomer, '/customers/<customer_id>')

