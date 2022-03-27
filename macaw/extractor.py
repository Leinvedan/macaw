import re
import requests
import hashlib
import time
from parsel import Selector
from os.path import exists

NUMBER_REGEX = '\$?[+-]?[0-9]{1,3}(?:[0-9]*(?:[.,][0-9]+)?|(?:,[0-9]{3})*(?:\.[0-9]{2})?|(?:\.[0-9]{3})*(?:,[0-9]{2})?)'
ASSET_REGEX = 'VCPU|CPU|MEMORY|STORAGE|SSD DISK|BANDWIDTH|TRANSFER|\/mo|\/hr'
UNIT_REGEX = 'TB|GB'


def extract_links(html: str, keywords: list[str] = []) -> list[str]:
    '''
    Extracts a list of links from the given HTML
    The search criteria is based on the keywords.
    Duplicates are filtered out
    '''
    result = []
    selector = Selector(html)
    links = selector.css('a').xpath('@href').getall()

    result = filter(lambda link: _keyword_filter(link, keywords), links)
    result = list(set(result)) # remove duplicates
    return result


def _keyword_filter(link: str, keywords: list[str]) -> bool:
    bool_list = [word in link for word in keywords]
    return all(bool_list)


def extract_plans(html: str) -> list[dict[str, str]]:
    '''
    Extracts all the plans in the HTML. Each plan is composed by
    resources. The return structure is the following:
    ```python
    [ # list of plans
        {
            'Storage': '500GB',
             "Memory": "1GB"
        },
    ]
    ```
    '''
    extracted = []
    row_css = 'div[class*=pt__row-content]'
    price_css = 'div[class*=js-price]'
    selector = Selector(html)

    plan_nodes = selector.css(row_css).getall()
    for idx, plan in enumerate(plan_nodes):
        selector = Selector(plan)

        resource_nodes = selector.css(price_css).getall()
        for resource in resource_nodes:
            value = re.search(NUMBER_REGEX, resource)
            value_unit = re.search(UNIT_REGEX, resource)
            resource_type = re.search(ASSET_REGEX, resource, re.IGNORECASE)

            if value and resource_type:
                resource_type = resource_type.group()
                value = value.group()

                if value_unit:
                    value = f'{value}{value_unit.group()}'

                if len(extracted) - 1 < idx:
                    extracted.append({})

                extracted[idx][f'{resource_type}'] = value

    return extracted


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
