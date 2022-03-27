import requests
import hashlib
import time
from os.path import exists
from typing import Any
from macaw.configs import PageType


def get_content(url: str) -> tuple[Any, str]:
    '''
    Returns a tuple with `content type` and 
    `local cached` content to avoid multiple requests
    on the same page.
    
    - return: `(type: PageType, content: str)`

    If the cache is not found, then `a request is made` to the url
    '''
    try:
        cache_key = hashlib.sha224(bytes(url, 'UTF-8')).hexdigest()
        file_type = _get_file_type(url)
        file = f'cache/{cache_key}.{file_type.value}'

        if exists(file):
            with open(file, 'r') as f:
                print(f'returning cached version of {url}')
                return (f.read(), file_type)

        time.sleep(1)  # Avoid requesting too fast
        r = requests.get(url)
        with open(file, 'w') as f:
            f.write(r.text)
            print(f'retuning fresh version of {url}')
            return (r.text, file_type)
    except Exception as err:
        print(f"Error using {url}: {err}")
        raise Exception(err)


def _get_file_type(url: str) -> Any:
    '''
    Returns a `PageType` enum with the 
    url's target page type (js, html)
    '''
    if '.js' in url:
        return PageType.JS
    return PageType.HTML