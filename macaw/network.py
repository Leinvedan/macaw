import time
import logging
import hashlib
from os.path import exists
import requests


def get_content(url: str) -> str:
    '''
    Returns a tuple with `content type` and
    `local cached` content to avoid multiple requests
    on the same page.

    - return: `(type: PageType, content: str)`

    If the cache is not found, then `a request is made` to the url
    '''
    try:
        cache_key = hashlib.sha224(bytes(url, 'UTF-8')).hexdigest()
        file = f'cache/{cache_key}.{_get_file_type(url)}'

        if exists(file):
            with open(file, 'r', encoding='UTF-8') as file:
                logging.info(f'returning cached version of {url}')
                return file.read()

        time.sleep(1)  # Avoid requesting too fast

        response = requests.get(url)
        with open(file, 'w', encoding='UTF-8') as file:
            file.write(response.text)
            logging.info(f'retuning fresh version of {url}')
            return response.text

    except Exception as err:
        logging.error(f"Error using {url}: {err}")
        raise Exception(err) from err


def _get_file_type(url: str) -> str:
    '''
    Returns a `PageType` enum with the
    url's target page type (js, html)
    '''
    if '.js' in url:
        return 'js'
    return 'html'
