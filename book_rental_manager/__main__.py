import argparse

from book_rental_manager.app import app
from book_rental_manager.database import init_db


def argument_parser():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers(title='sub_parser')
    parser.set_defaults(parser=None)

    init_parser = sub_parser.add_parser('init')
    init_parser.add_argument('-a', '--all', action='store_true')
    init_parser.set_defaults(parser='init')

    run_app = sub_parser.add_parser('server')
    run_app.add_argument('-a', '--address', default='localhost', 
                         help='host address')
    run_app.add_argument('-p', '--port', type=int, default=5000, 
                         help='port')
    run_app.add_argument('-d', '--debug', action='store_true')
    run_app.set_defaults(parser='server')

    return parser  

if __name__ == '__main__':
    parser = argument_parser()
    argspec = parser.parse_args()  
    print(argspec)
    if argspec.parser == 'init':
        init_db()
    elif argspec.parser == 'server':
        app.run(host=argspec.address,
                port=argspec.port,
                debug=argspec.debug)
    else:
        parser.print_help()
    