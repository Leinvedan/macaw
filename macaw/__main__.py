from pathlib import Path
from macaw.extractor import extract_links, extract_plans, get_html
from macaw.writer import get_writer_function
from macaw.normalizer import normalize_plan


def main():
    write_data = get_writer_function()

    domain = 'https://www.vultr.com'
    path = '/products/cloud-compute/#pricing'
    keywords = ['/pricing', 'cloud']

    plans = start_crawling(domain, path, keywords)

    write_data(plans)


def start_crawling(domain: str, path: str = '', keywords: list[str] = []) -> list[dict[str, str]]:
    landing_page = get_html(f'{domain}{path}')
    pricing_links = extract_links(landing_page, keywords)

    if not pricing_links:
        print("Link not found")
        return

    prices = []
    for link in pricing_links:
        # FIXME! Sobrando tempo, fazer um mapa de links visitados
        # e colocar a busca de links também num loop
        next_page_html = get_html(f'{domain}{link}')

        page_prices = extract_plans(next_page_html)
        page_prices = [normalize_plan(plan) for plan in page_prices]

        prices = prices + page_prices

    return prices


if __name__ == '__main__':
    Path("cache").mkdir(exist_ok=True)
    main()
