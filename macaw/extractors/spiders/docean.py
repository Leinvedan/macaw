import re
import json


SIZE_ID_REGEX = r'{size_id:"\d+"+.*?}}}'
RESOURCE_REGEX_TEMPLATE = r'\{{.+?\$"\.concat\(Vt\("droplet","{}".+?(?<=\)\),)(?P<resource>.+?(?=}}))'
CAT_REGULAR_REGEX = r'[{|,]regular.+?}]'
CAT_PREMIUM_AMD_REGEX = r'[{|,]premiumAMD.+?}]'
CAT_PREMIUM_INTEL_REGEX = r'[{|,]premiumIntel.+?}]'


def parse_js(js_file: str) -> list[dict[str, str]]:
    '''
    Extracts information from docean javascript file.
    The montly prices are separated from the machine resources
    this function will merge them and return the dictionary
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
    # of the data
    first_halfs = re.findall(SIZE_ID_REGEX, js_file)

    for category in categories:
        extracted = _extract_from_docean_category(category, first_halfs)
        result = result + extracted

    return result


def _extract_from_docean_category(category: str, first_halfs) -> dict[str, str]:
    results = []

    for first_half in first_halfs:
        first_half = _js_to_json(first_half)

        # build regex to get the second_half
        # using size_id
        size_id = first_half['size_id']
        regex = RESOURCE_REGEX_TEMPLATE.format(size_id)

        second_half = re.search(regex, category)
        if not second_half:
            continue

        second_half = second_half.group('resource')
        second_half = f'{{{second_half}}}'
        second_half = _js_to_json(second_half)

        results.append({
            'usd_rate_per_month': first_half['item_price']['usd_rate_per_month'],
            **second_half
        })
    return results


def _js_to_json(js_data: str):
    KEY_REGEX = '[{,](.*?):'
    keys = re.findall(KEY_REGEX, js_data)
    for key in keys:
        js_data = js_data.replace(f'{key}', f'"{key}"')
    return json.loads(js_data)
