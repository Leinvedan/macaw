import re
from parsel import Selector

# pylint:disable=line-too-long
NUMBER_REGEX = r'\$?[+-]?[0-9]{1,3}(?:[0-9]*(?:[.,][0-9]+)?|(?:,[0-9]{3})*(?:\.[0-9]{2})?|(?:\.[0-9]{3})*(?:,[0-9]{2})?)'
ASSET_REGEX = r'VCPU|CPU|MEMORY|STORAGE|SSD DISK|BANDWIDTH|TRANSFER|\/mo|\/hr'
UNIT_REGEX = r'TB|GB'


def parse_html(html: str) -> list[dict[str, str]]:
    '''
    Extracts all the plans in the Vultr HTML.
    Each plan is composed by resources.
    The return structure is the following:
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

                if resource_type.lower() in ['cpu', 'vcpu']:
                    value = f'{value}{resource_type}'


                if len(extracted) - 1 < idx:
                    extracted.append({})

                extracted[idx][f'{resource_type}'] = value

    return extracted
