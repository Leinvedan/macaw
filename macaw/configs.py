from enum import Enum

class PageType(Enum):
    HTML='html'
    JS='js'

HREF_XPATH = '//a/@href'
SCRIPT_XPATH = '//script/@src'

FIELD_NAMES = ['CPU / VCPU', 'MEMORY', 'STORAGE / SSD DISK',
               'BANDWIDTH / TRANSFER', 'PRICE [$/mo]']


VULTR_CONFIG = {
    'domain': 'https://www.vultr.com',
    'path': '/products/cloud-compute/#pricing',
    'link_query': {
        'keywords': ['/pricing', 'cloud'],
        'xpath': HREF_XPATH
    }
}

DOCEAN_CONFIG = {
    'domain': 'https://www.digitalocean.com',
    'path': '/pricing',
    'link_query': {
        'keywords': ['/_next/static/chunks/pages/pricing-'],
        'xpath': SCRIPT_XPATH
    }
}