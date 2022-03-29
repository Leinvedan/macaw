import logging
import asyncio
from pathlib import Path
from typing import Callable
from macaw.network import get_content
from macaw.writer import get_writer_function
from macaw.normalizer import normalize_plan
from macaw.configs import VULTR_CONFIG, DOCEAN_CONFIG
from macaw.extractors.links import extract_links


async def main():
    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s',
                        level=logging.INFO)
    logging.info('Starting Macaw!')
    write_data = get_writer_function()

    result = await asyncio.gather(
        start_crawling(**VULTR_CONFIG),
        start_crawling(**DOCEAN_CONFIG)
    )

    # flatten the result
    plans = [item for sublist in result for item in sublist]

    write_data(plans)


async def start_crawling(origin: str, run_spider: Callable, url: dict[str, str],
                   link_query: dict[str, str]) -> list[dict[str, str]]:
    domain = url['domain']
    path = url['path']

    landing_page = await get_content(f'{domain}{path}', sleep=0)
    pricing_links = extract_links(landing_page, **link_query)

    if not pricing_links:
        logging.error("Link not found! Check your config's keywords and xpath")
        return []

    prices = []
    for link in pricing_links:

        next_page = await get_content(f'{domain}{link}', sleep=1)
        page_prices = run_spider(next_page)

        if page_prices:
            page_prices = [normalize_plan(plan, origin)
                           for plan in page_prices]
            prices = prices + page_prices

    return prices


if __name__ == '__main__':
    Path("cache").mkdir(exist_ok=True)
    asyncio.run(main())
