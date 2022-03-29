import sys
import json
import csv
import logging
from typing import Callable
from macaw.configs import FIELD_NAMES

OUT_FILENAME = 'plans'


def get_writer_function() -> Callable:
    '''
    Returns the function that will write the parameter data
    in the respective output of the given commandline argument.
    '''

    if len(sys.argv) < 2:
        logging.warning('Please choose a output argument')
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
        case '--save_csv':
            return write_as_csv
        case _:
            logging.error('Invalid argument')
            print_help()
            sys.exit(1)


def print_help():
    logging.info('--print: prints the result in stdout')
    logging.info('--save_json: saves the result as plans.json file')


def write_as_json(data: list[dict[str, str]]):
    result = json.dumps(data, indent=2)
    with open(f'{OUT_FILENAME}.json', 'w', encoding='UTF-8') as file:
        file.write(result)


def write_as_csv(data: list[dict[str, str]]):
    with open(f'{OUT_FILENAME}.csv', 'w', encoding='UTF-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(data)
