import sys
import json
from typing import Callable


def get_save_function() -> Callable:
    '''
    Returns the function that will save the output
    based on the given commandline argument.
    '''

    if len(sys.argv) < 2:
        exit_program()

    match sys.argv[1]:
        case '--print':
            return print
        case '--to_json':
            return save_as_json
        case _:
            exit_program()

def exit_program():
    print('Please choose a output argument')
    print('--print: prints the result in stdout')
    print('--to_json: saves the result as plans.json file')
    sys.exit(0)

def save_as_json(data: list[list[dict[str, str]]]):
    result = json.dumps(data, indent=2)
    with open('plans.json', 'w') as f:
        f.write(result)
