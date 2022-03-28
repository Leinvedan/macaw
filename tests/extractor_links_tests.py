import unittest
from macaw.extractors.links import extract_links
from macaw.configs import HREF_XPATH, SCRIPT_XPATH

FIXTURE_PATH = 'tests/fixtures'
RESULT_PATH = 'tests/results'


class ExtractLinkTestCase(unittest.TestCase):
    def setUp(self):
        with open(f'{FIXTURE_PATH}/vultr_1.html', 'r') as f:
            self.vultr_1 = f.read()
        with open(f'{FIXTURE_PATH}/docean_1.html', 'r') as f:
            self.docean_1 = f.read()

    def test_extract_link_vultr_1(self):
        keywords = ['/pricing', 'cloud']
        expected_links = ['/pricing/cloud', '/pricing/#cloud-compute/']

        links = extract_links(self.vultr_1, HREF_XPATH, keywords)

        self.assertEqual(len(links), len(expected_links))
        self.assertTrue(expected_links[0] in links)
        self.assertTrue(expected_links[1] in links)

    def test_extract_link_docean_1(self):
        keywords = ['/_next/static/chunks/pages/pricing-']
        expected_link = '/_next/static/chunks/pages/pricing-1a7cdb1f9a255535.js'

        links = extract_links(self.docean_1, SCRIPT_XPATH, keywords)

        self.assertEqual(len(links), 1)
        self.assertTrue(expected_link in links)

if __name__ == '__main__':
    unittest.main()
