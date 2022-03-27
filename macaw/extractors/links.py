from parsel import Selector

def extract_links(html: str, xpath: str, keywords: list[str] = []) -> list[str]:
    '''
    Extracts a list of links from the given HTML
    The search criteria is based on the keywords.
    Duplicates are filtered out
    '''
    result = []
    selector = Selector(html)
    links = selector.xpath(xpath).getall()

    result = filter(lambda link: _keyword_filter(link, keywords), links)
    result = list(set(result)) # remove duplicates
    return result


def _keyword_filter(link: str, keywords: list[str]) -> bool:
    bool_list = [word in link for word in keywords]
    return all(bool_list)