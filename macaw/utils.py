import sys
import json
from typing import Callable


def get_save_function() -> Callable:
    '''
    Returns the function that will save the output
    based on the given commandline argument.
    '''

    if len(sys.argv) < 2:
        print('Please choose a output argument')
        print_help()
        sys.exit(1)

    match sys.argv[1]:
        case '--help':
            print_help()
            sys.exit(0)
        case '--print':
            return print
        case '--to_json':
            return save_as_json
        case _:
            print('Invalid argument')
            print_help()
            sys.exit(1)


def print_help():
    print('--print: prints the result in stdout')
    print('--to_json: saves the result as plans.json file')

def save_as_json(data: list[dict[str, str]]):
    result = json.dumps(data, indent=2)
    with open('plans.json', 'w') as f:
        f.write(result)
