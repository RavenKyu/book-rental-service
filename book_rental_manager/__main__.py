import argparse

from book_rental_manager.app import app
from book_rental_manager.database import init_db


def argument_parser():
    parser = argparse.ArgumentParser()

    sub_parser = parser.add_subparsers(dest='sub_parser')
    init_parser = sub_parser.add_parser('init', help='Initialize Database')

    run_app = sub_parser.add_parser('server', help='Run the api server')
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
        init_db()
    elif argspec.sub_parser == 'server':
        app.run(host=argspec.address,
                port=argspec.port,
                debug=argspec.debug)
    else:
        parser.print_help()
    