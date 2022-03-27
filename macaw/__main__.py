from pathlib import Path
import time
from macaw.extractor import extract_link, extract_plans, get_html
from macaw.utils import get_save_function


# TODO:
# Verificar se tem os preços
# Caso não tenha, crawlear todos os link com
# palavras chave: [pricing, cloud] (manter uma lista de links visitados)
# repetir até achar os preços

def main():
    save = get_save_function()
    domain = 'https://www.vultr.com'

    landing_page = get_html(f'{domain}/products/cloud-compute/#pricing')
    pricing_link = extract_link(landing_page)

    if not pricing_link:
        print("Link not found")
        return

    time.sleep(1)  # Avoid requesting to same domain too fast

    next_page_html = get_html(f'{domain}{pricing_link}')
    prices = extract_plans(next_page_html)

    save(prices)


if __name__ == '__main__':
    Path("cache").mkdir(exist_ok=True)
    main()
