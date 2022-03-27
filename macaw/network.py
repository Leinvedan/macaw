import requests
import hashlib
import time
from os.path import exists


def get_html(url: str) -> str:
    '''
    Returns local cached HTML to avoid multiple requests
    on the same page.

    If the cache is not found, then the request is made to the url
    '''
    try:
        cache_key = hashlib.sha224(bytes(url, 'UTF-8')).hexdigest()
        file = f'cache/{cache_key}.html'

        if exists(file):
            with open(file, 'r') as f:
                print(f'returning cached version of {url}')
                return f.read()

        time.sleep(1)  # Avoid requesting too fast
        r = requests.get(url)
        with open(file, 'w') as f:
            f.write(r.text)
            print(f'retuning fresh version of {url}')
            return r.text
    except Exception as err:
        print(f"Error using {url}: {err}")
        raise Exception(err)
