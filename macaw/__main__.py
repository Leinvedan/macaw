from pathlib import Path
from macaw.network import get_content
from macaw.writer import get_writer_function
from macaw.normalizer import normalize_plan
from macaw.configs import VULTR_CONFIG, DOCEAN_CONFIG
from macaw.extractors.links import extract_links
from macaw.extractors.plans import extract_plans


def main():
    write_data = get_writer_function()
    plans = start_crawling(**VULTR_CONFIG)
    # plans = start_crawling(docean_config)

    write_data(plans)

def start_crawling(domain: str, path: str, link_query: dict[str, str]) -> list[dict[str, str]]:

    landing_page, _ = get_content(f'{domain}{path}')
    pricing_links = extract_links(landing_page, **link_query)

    if not pricing_links:
        print("Link not found")
        return

    prices = []
    for link in pricing_links:
        # FIXME! Sobrando tempo, fazer um mapa de links visitados
        # e colocar a busca de links também num loop

        next_page, page_type = get_content(f'{domain}{link}')

        page_prices = extract_plans(next_page, page_type)
        if page_prices:
            page_prices = [normalize_plan(plan) for plan in page_prices]
            prices = prices + page_prices

    return prices


if __name__ == '__main__':
    Path("cache").mkdir(exist_ok=True)
    main()
