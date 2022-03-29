import asyncio
import logging
import hashlib
from os.path import exists
import aiohttp


async def get_content(url: str, sleep: int=0) -> str:
    '''
    Returns a tuple with `local cached` content.

    To avoid multiple requests on the same page, a cached
    copy is returned, if available.

    If there's no cache, the function will wait
    `sleep` seconds and makes a HTTP GET request to the url
    '''
    try:
        cache_key = hashlib.sha224(bytes(url, 'UTF-8')).hexdigest()
        file = f'cache/{cache_key}.{_get_file_type(url)}'

        if exists(file):
            with open(file, 'r', encoding='UTF-8') as file:
                logging.info(f'returning cached version of {url}')
                return file.read()

        await asyncio.sleep(sleep)  # Avoid requesting too fast

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                with open(file, 'w', encoding='UTF-8') as file:
                    content = await response.text()
                    logging.info(f'caching {url}')
                    file.write(content)
                    logging.info(f'using fresh version of {url}')
                    return content

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
