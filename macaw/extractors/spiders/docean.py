import re
import json

CAT_REGULAR_REGEX = r'[{|,]regular.+?}]'
CAT_PREMIUM_AMD_REGEX = r'[{|,]premiumAMD.+?}]'
CAT_PREMIUM_INTEL_REGEX = r'[{|,]premiumIntel.+?}]'

SIZE_ID_REGEX = r'{size_id:"\d+"+.*?}}}'
MONTHLY_PRICE_REGEX = r'{priceMo.+?}'
MONTHLY_PRICE_ID_REGEX = r'"(?P<value>\d+)"'

KEY_TEMPLATE_REGEX = '{}:"(?P<value>.+?)"'

RESOURCE_KEYS = [
    'cpuAmount',
    'cpuType',
    'ssdAmount',
    'transferAmount'
]


def parse_js(js_file: str) -> list[dict[str, str]]:
    '''
    Extracts information from docean javascript file.
    The montly prices are separated from the machine resources
    this function will merge them and return the dictionary.
    '''
    result = []
    categories = []

    regular = re.search(CAT_REGULAR_REGEX, js_file)
    amd = re.search(CAT_PREMIUM_AMD_REGEX, js_file)
    intel = re.search(CAT_PREMIUM_INTEL_REGEX, js_file)

    if regular:
        categories.append(regular.group())
    if amd:
        categories.append(amd.group())
    if intel:
        categories.append(intel.group())

    # parse json with size_ids to get first_half
    # of the data as month_price_jsons
    #
    # the monthly prices
    # are shared between categories
    month_price_jsons = re.findall(SIZE_ID_REGEX, js_file)

    # Build a price_map for each category
    # then merge it's data with the monthly price
    # matching both by their size_id
    for category in categories:
        prices_map = _build_prices_map(category)
        extracted = _merge_price_datas(month_price_jsons, prices_map)
        result = result + extracted

    return result


def _build_prices_map(category) -> dict[str, list[str]]:
    '''
    returns the following map:

    {
        <size_id>: <price_data_str>
    }

    To match with monthly prices data.
    '''
    result = {}
    second_halfs = re.findall(MONTHLY_PRICE_REGEX, category)

    for half in second_halfs:
        size_id = re.search(MONTHLY_PRICE_ID_REGEX, half)
        if size_id:
            size_id = size_id.group('value')
            result[size_id] = half

    return result


def _merge_price_datas(month_price_jsons: list[str],
                       prices_map: dict[str, list[str]]) -> dict[str, str]:
    '''
    Iterates each size_id from monthly prices
    and tries to match with all price_data inside the
    corresponding price_map value
    '''
    results = []

    for month_price_json in month_price_jsons:

        month_price_json = _js_to_dict(month_price_json)
        size_id = month_price_json['size_id']

        if size_id not in prices_map:
            continue

        resource_str = prices_map[size_id]
        if resource_str:
            resource = extract_entries(resource_str)

            results.append({
                'usd_rate_per_month': month_price_json['item_price']['usd_rate_per_month'],
                **resource
            })

    return results


def _js_to_dict(js_data: str):
    key_regex = '[{,](.*?):'
    keys = re.findall(key_regex, js_data)
    for key in keys:
        js_data = js_data.replace(f'{key}', f'"{key}"')
    return json.loads(js_data)


def extract_entries(data: str) -> dict[str, str]:
    '''
    Extract each key from `RESOURCE_KEYS` and
    return them inside a `dict`
    '''
    result = {}
    for key_name in RESOURCE_KEYS:
        regex = KEY_TEMPLATE_REGEX.format(key_name)
        value = re.search(regex, data)
        if value:
            result[key_name] = value.group('value')
    return result
