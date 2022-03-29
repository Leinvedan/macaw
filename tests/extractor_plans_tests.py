import unittest
import json
from macaw.extractors.spiders.docean import parse_js as parse_docean_js
from macaw.extractors.spiders.vultr import parse_html as parse_vultr_html
from macaw.normalizer import normalize_plan


FIXTURE_PATH = 'tests/fixtures'
RESULT_PATH = 'tests/results'


class ExtractTestCase(unittest.TestCase):
    def setUp(self):
        self.origin = 'test'
        with open(f'{FIXTURE_PATH}/vultr_1.html', 'r', encoding='UTF-8') as file:
            self.vultr_1 = file.read()
        with open(f'{FIXTURE_PATH}/docean_1.html', 'r', encoding='UTF-8') as file:
            self.docean_1 = file.read()
        with open(f'{FIXTURE_PATH}/docean_2.js', 'r', encoding='UTF-8') as file:
            self.docean_2 = file.read()

    def test_extract_prices_all_values(self):
        plans = parse_vultr_html(self.vultr_1)
        plans = [normalize_plan(plan, self.origin) for plan in plans]
        total_machines = 16
        expected = None
        # with open(f'{RESULT_PATH}/vultr_1.json', 'w') as f:
        #     f.write(json.dumps(plans))
        with open(f'{RESULT_PATH}/vultr_1.json', 'r', encoding='UTF-8') as file:
            expected = json.loads(file.read())

        self.assertEqual(plans, expected)
        self.assertEqual(len(plans), total_machines)

    def test_item_exists_inside_prices(self):
        plans = parse_vultr_html(self.vultr_1)
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

    def test_docean_js_extractor(self):
        plans = parse_docean_js(self.docean_2)
        plans = [normalize_plan(plan, self.origin) for plan in plans]

        with open(f'{RESULT_PATH}/docean_2.json', 'r', encoding='UTF-8') as file:
            expected = json.loads(file.read())

        self.assertEqual(plans, expected)


if __name__ == '__main__':
    unittest.main()
