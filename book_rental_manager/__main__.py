import argparse

import faker
from book_rental_manager.app import app
from book_rental_manager.database import (init_db, dummy_members, dummy_books)


def argument_parser():
    parser = argparse.ArgumentParser('book-rental-manager-api')

    sub_parser = parser.add_subparsers(dest='sub_parser')
    init_parser = sub_parser.add_parser('init', help='Initialize database')
    init_parser.add_argument('-d', '--init-db', action='store_true',
                             help='initialize database.')
    init_parser.add_argument('-m', '--dummy-members', action='store_true',
                             help='insert dummy members.')
    init_parser.add_argument('-b', '--dummy-books', action='store_true',
                             help='insert dummy books.')

    run_app = sub_parser.add_parser('server', help='Run api server')
    run_app.add_argument('-a', '--address', default='localhost', 
                         help='host address')
    run_app.add_argument('-p', '--port', type=int, default=5000, 
                         help='port')
    run_app.add_argument('-d', '--debug', action='store_true')
    
    return parser  

if __name__ == '__main__':
    parser = argument_parser()
    argspec = parser.parse_args()  
    print(argspec)
    if argspec.sub_parser == 'init':
        
        if argspec.init_db:
            init_db()
        if argspec.dummy_members:
            dummy_members()
        if argspec.dummy_books:
            dummy_books()

    elif argspec.sub_parser == 'server':
        app.run(host=argspec.address,
                port=argspec.port,
                debug=argspec.debug)
    else:
        parser.print_help()
    