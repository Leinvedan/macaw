import unittest
from macaw.extractors.plans import extract_plans
from macaw.configs import PageType

FIXTURE_PATH = 'tests/fixtures'
RESULT_PATH = 'tests/results'


class ExtractTestCase(unittest.TestCase):
    def setUp(self):
        with open(f'{FIXTURE_PATH}/vultr_1.html', 'r') as f:
            self.vultr_1 = f.read()
        with open(f'{FIXTURE_PATH}/docean_1.html', 'r') as f:
            self.docean_1 = f.read()

    def test_extract_prices_all_values(self):
        prices = extract_plans(self.vultr_1, PageType.HTML)
        total_machines = 16
        expected = None
        # with open(f'{RESULT_PATH}/vultr_1.txt', 'w') as f:
        #     f.write(str(prices))
        with open(f'{RESULT_PATH}/vultr_1.txt', 'r') as f:
            expected = f.read()

        self.assertEqual(str(prices), expected)
        self.assertEqual(len(prices), total_machines)

    def test_item_exists_inside_prices(self):
        plans = extract_plans(self.vultr_1, PageType.HTML)
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
