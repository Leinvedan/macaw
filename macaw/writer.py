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

    command = ''
    if len(sys.argv) < 2:
        logging.warning('Please choose a output argument')
        _print_help()
        command = _get_command()
    else:
        command = sys.argv[1]

    match command:
        case '--help':
            _print_help()
            sys.exit(0)
        case '--print':
            return print
        case '--save_json':
            return _write_as_json
        case '--save_csv':
            return _write_as_csv
        case _:
            logging.error('Invalid argument')
            _print_help()
            sys.exit(1)

def _get_command():
    try:
        while True:
            command = input('command: ')
            if command in ['--print', '--save_json', '--save_csv']:
                break
    except KeyboardInterrupt:
        logging.info('Quitting application...')
        sys.exit(0)

    return command


def _print_help():
    logging.info('--print: prints the result in stdout')
    logging.info('--save_json: saves the result as plans.json file')
    logging.info('--save_csv: saves the result as plans.csv file')


def _write_as_json(data: list[dict[str, str]]):
    result = json.dumps(data, indent=2)
    with open(f'{OUT_FILENAME}.json', 'w', encoding='UTF-8') as file:
        file.write(result)


def _write_as_csv(data: list[dict[str, str]]):
    with open(f'{OUT_FILENAME}.csv', 'w', encoding='UTF-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(data)
