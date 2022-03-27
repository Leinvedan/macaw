import sys
import json
from typing import Callable


def get_write_function() -> Callable:
    '''
    Returns the function that will write the parameter data
    in the respective output of the given commandline argument.
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
        case '--save_json':
            return write_as_json
        case _:
            print('Invalid argument')
            print_help()
            sys.exit(1)


def print_help():
    print('--print: prints the result in stdout')
    print('--save_json: saves the result as plans.json file')

def write_as_json(data: list[dict[str, str]]):
    result = json.dumps(data, indent=2)
    with open('plans.json', 'w') as f:
        f.write(result)
