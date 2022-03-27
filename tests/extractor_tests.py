import unittest
from test import support
from macaw.extractor import extract_plans, extract_link

FIXTURE_PATH = 'tests/fixtures'
RESULT_PATH = 'tests/results'


class MyTestCase1(unittest.TestCase):
    def setUp(self):
        with open(f'{FIXTURE_PATH}/vultr_1.html', 'r') as f:
            self.vultr_1 = f.read()
    
    def test_extract_link(self):
        link = extract_link(self.vultr_1)
        expected_link = '/pricing/cloud'
        self.assertEqual(link, expected_link)

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
                'type': '/hr',
                'value': '$0.143',
            },
            {
                'type': 'Bandwidth',
                'value': '5.00TB'
            },
            {
                'type': 'Storage',
                'value': '500000000GB'
            }]

        found_entries = 0
        for plan in plans:
            for resource in expected_resources:
                if resource in plan:
                    found_entries += 1

        self.assertEqual(found_entries, number_of_matching_resources)


if __name__ == '__main__':
    unittest.main()
