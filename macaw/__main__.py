from pathlib import Path
from typing import Callable
from macaw.network import get_content
from macaw.writer import get_writer_function
from macaw.normalizer import normalize_plan
from macaw.configs import VULTR_CONFIG, DOCEAN_CONFIG
from macaw.extractors.links import extract_links


def main():
    write_data = get_writer_function()
    plans_vultr = start_crawling(**VULTR_CONFIG)
    plans_docean = start_crawling(**DOCEAN_CONFIG)
    plans = plans_vultr + plans_docean

    write_data(plans)


def start_crawling(origin: str, run_spider: Callable, url: dict[str, str],
                   link_query: dict[str, str]) -> list[dict[str, str]]:
    domain = url['domain']
    path = url['path']

    landing_page = get_content(f'{domain}{path}')
    pricing_links = extract_links(landing_page, **link_query)

    if not pricing_links:
        print("Link not found")
        return []

    prices = []
    for link in pricing_links:

        next_page = get_content(f'{domain}{link}')
        page_prices = run_spider(next_page)

        if page_prices:
            page_prices = [normalize_plan(plan, origin)
                           for plan in page_prices]
            prices = prices + page_prices

    return prices


if __name__ == '__main__':
    Path("cache").mkdir(exist_ok=True)
    main()
