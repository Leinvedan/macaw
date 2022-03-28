import re
import json
from parsel import Selector
from macaw.configs import PageType

# vultr specific regexes
NUMBER_REGEX = '\$?[+-]?[0-9]{1,3}(?:[0-9]*(?:[.,][0-9]+)?|(?:,[0-9]{3})*(?:\.[0-9]{2})?|(?:\.[0-9]{3})*(?:,[0-9]{2})?)'
ASSET_REGEX = 'VCPU|CPU|MEMORY|STORAGE|SSD DISK|BANDWIDTH|TRANSFER|\/mo|\/hr'
UNIT_REGEX = 'TB|GB'

# DOcean specific regexes
SIZE_ID_REGEX = '{size_id:"\d+"+.*?}}}'
RESOURCE_REGEX_TEMPLATE = '\{{.+?\$"\.concat\(Vt\("droplet","{}".+?(?<=\)\),)(?P<resource>.+?(?=}}))'
CAT_REGULAR_REGEX = '[{|,]regular.+?}]'
CAT_PREMIUM_AMD_REGEX = '[{|,]premiumAMD.+?}]'
CAT_PREMIUM_INTEL_REGEX = '[{|,]premiumIntel.+?}]'


def extract_plans(content: str, content_type: str) -> list[dict[str, str]]:
    match content_type:
        case PageType.HTML:
            return extract_from_html(content)
        case PageType.JS:
            return extract_from_docean_js(content)
    return


def extract_from_html(html: str) -> list[dict[str, str]]:
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


def extract_from_docean_js(file: str) -> list[dict[str, str]]:
    '''
    Extracts information from docean javascript file.
    The montly prices are separated from the machine resources
    this function will merge them and return the dictionary
    '''
    result = []
    categories = []

    regular = re.search(CAT_REGULAR_REGEX, file)
    amd = re.search(CAT_PREMIUM_AMD_REGEX, file)
    intel = re.search(CAT_PREMIUM_INTEL_REGEX, file)

    if regular:
        categories.append(regular.group())
    if amd:
        categories.append(amd.group())
    if intel:
        categories.append(intel.group())

    # parse json with size_ids to get first_half
    # of the data
    first_halfs = re.findall(SIZE_ID_REGEX, file)

    for category in categories:
        extracted = _extract_from_docean_category(category, first_halfs)
        result = result + extracted

    return result


def _extract_from_docean_category(category: str, first_halfs) -> dict[str, str]:
        results = []

        for first_half in first_halfs:
            first_half = js_to_json(first_half)

            # build regex to get the second_half
            # using size_id
            size_id = first_half['size_id']
            regex = RESOURCE_REGEX_TEMPLATE.format(size_id) 

            
            second_half = re.search(regex, category)
            if not second_half:
                continue

            second_half = second_half.group('resource')
            second_half = f'{{{second_half}}}'
            second_half = js_to_json(second_half)


            results.append({
                'usd_rate_per_month': first_half['item_price']['usd_rate_per_month'],
                **second_half
            })
        return results


def js_to_json(js_data: str):
    KEY_REGEX = '[{,](.*?):'
    keys = re.findall(KEY_REGEX, js_data)
    for key in keys:
        js_data = js_data.replace(f'{key}', f'"{key}"')
    return json.loads(js_data)