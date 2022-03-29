from macaw.extractors.spiders.docean import parse_js as parse_docean_js
from macaw.extractors.spiders.vultr import parse_html as parse_vultr_html

HREF_XPATH = '//a/@href'
SCRIPT_XPATH = '//script/@src'

FIELD_NAMES = ['ORIGIN','CPU / VCPU', 'MEMORY', 'STORAGE / SSD DISK',
               'BANDWIDTH / TRANSFER', 'PRICE [$/mo]']


VULTR_CONFIG = {
    'origin': 'vultr',
    'run_spider': parse_vultr_html,
    'url': {
        'domain': 'https://www.vultr.com',
        'path': '/products/cloud-compute/#pricing',
    },
    'link_query': {
        'keywords': ['/pricing', 'cloud'],
        'xpath': HREF_XPATH
    }
}

DOCEAN_CONFIG = {
    'origin': 'docean',
    'run_spider': parse_docean_js,
    'url': {
        'domain': 'https://www.digitalocean.com',
        'path': '/pricing',
    },
    'link_query': {
        'keywords': ['/_next/static/chunks/pages/pricing-'],
        'xpath': SCRIPT_XPATH
    }
}
