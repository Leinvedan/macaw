from macaw.extractors.spiders.docean import parse_js as parse_docean_js
from macaw.extractors.spiders.vultr import parse_html as parse_vultr_html

HREF_XPATH = '//a/@href'
SCRIPT_XPATH = '//script/@src'

FIELD_NAMES = ['ORIGIN','CPU / VCPU', 'MEMORY', 'STORAGE / SSD DISK',
               'BANDWIDTH / TRANSFER', 'PRICE [$/mo]']


VULTR_CONFIG = {
    'origin': 'vultr',
    'domain': 'https://www.vultr.com',
    'path': '/products/cloud-compute/#pricing',
    'run_spider': parse_vultr_html,
    'link_query': {
        'keywords': ['/pricing', 'cloud'],
        'xpath': HREF_XPATH
    }
}

DOCEAN_CONFIG = {
    'origin': 'docean',
    'domain': 'https://www.digitalocean.com',
    'path': '/pricing',
    'run_spider': parse_docean_js,
    'link_query': {
        'keywords': ['/_next/static/chunks/pages/pricing-'],
        'xpath': SCRIPT_XPATH
    }
}