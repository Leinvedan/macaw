import unittest
from macaw.extractors.plans import extract_plans
from macaw.extractors.links import extract_links
from macaw.configs import HREF_XPATH, SCRIPT_XPATH

FIXTURE_PATH = 'tests/fixtures'
RESULT_PATH = 'tests/results'


class ExtractTestCase(unittest.TestCase):
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

    def test_extract_prices_all_values(self):
        prices = extract_plans(self.vultr_1)
        total_machines = 16
        expected = None
        # with open(f'{RESULT_PATH}/vultr_1.txt', 'w') as f:
        #     f.write(str(prices))
        with open(f'{RESULT_PATH}/vultr_1.txt', 'r') as f:
            expected = f.read()

        # Quando mudar pra json o diff vai ficar melhor
        self.assertEqual(str(prices), expected)
        self.assertEqual(len(prices), total_machines)

    def test_item_exists_inside_prices(self):
        plans = extract_plans(self.vultr_1)
        number_of_matching_resources = 5
        expected_resources = [
            {
                '/hr': '$0.143',
            },
            {
                'Bandwidth': '5.00TB'
            },
            {
                'Storage': '500000000GB'
            }]
        expected_resources = list(
            map(lambda r: list(r.items())[0], expected_resources))

        found_entries = 0
        for plan in plans:
            for resource in expected_resources:
                if resource in plan.items():
                    found_entries += 1

        self.assertEqual(found_entries, number_of_matching_resources)


if __name__ == '__main__':
    unittest.main()
