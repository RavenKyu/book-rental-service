import unittest
from book_rental_manager.database import Customer


class DataBaseTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test100_customers_tablename(self):
        self.assertEqual('customers', Customer.__tablename__)

    def test105_customers_add(self):
        c = Customer('Raven', '010-9508-0875')
        self.assertEqual('Raven', c.customer_name)
        self.assertEqual('010-9508-0875', c.customer_phone)
        