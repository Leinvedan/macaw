from macaw.constants import HREF_XPATH, SCRIPT_XPATH

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