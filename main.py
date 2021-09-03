from sys import argv
import sys
from app.index import UpdateIndexes


if __name__ == "__main__":
    if len(argv) == 1:
        print('usage: python3 main.py [r | l | ...]')
        print('i | Update indexes')
        print('dev | Run developer mode function')
    elif len(argv) >= 2:
        if argv[1] == 'i':
            update_indexes = UpdateIndexes()
            update_indexes.run()
        elif argv[1] == 'dev':
            print('This is a dev')
            # ...
            print('Dev is done')
        else:
            print('Wrong option')
    else:
        print('Wrong selection')