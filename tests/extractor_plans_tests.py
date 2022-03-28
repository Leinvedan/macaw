import unittest
from macaw.extractors.plans import extract_plans, extract_from_docean_js
from macaw.configs import PageType

FIXTURE_PATH = 'tests/fixtures'
RESULT_PATH = 'tests/results'


class ExtractTestCase(unittest.TestCase):
    def setUp(self):
        with open(f'{FIXTURE_PATH}/vultr_1.html', 'r') as f:
            self.vultr_1 = f.read()
        with open(f'{FIXTURE_PATH}/docean_1.html', 'r') as f:
            self.docean_1 = f.read()
        with open(f'{FIXTURE_PATH}/docean_2.js', 'r') as f:
            self.docean_2 = f.read()

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


    def test_docean_js_extractor(self):
        expected = [{'usd_rate_per_month': '96.00', 'cpuAmount': '1GB',
        'cpuType': '1vCPU', 'ssdAmount': '25GB', 'ssdType': 'SSD Disk',
        'transferAmount': '1000GB', 'link': 's-1vcpu-1gb'},
        {'usd_rate_per_month': '6.00', 'cpuAmount': '2GB', 'cpuType': '1vCPU',
        'ssdAmount': '50GB', 'ssdType': 'SSD Disk', 'transferAmount': '2TB',
        'link': 's-1vcpu-2gb'}, {'usd_rate_per_month': '18.00', 'cpuAmount': '8GB',
        'cpuType': '4vCPUs', 'ssdAmount': '160GB',
        'ssdType': 'SSD Disk', 'transferAmount': '5TB', 'link': 's-4vcpu-8gb'}, 
        {'usd_rate_per_month': '12.00', 'cpuAmount': '16GB', 'cpuType': '8 AMD CPUs',
        'ssdAmount': '320GB', 'ssdType': 'NVMe SSDs', 'transferAmount': '6TB',
        'link': 's-8vcpu-16gb-amd'}, {'usd_rate_per_month': '24.00', 'cpuAmount': '4GB',
        'cpuType': '2 AMD CPUs', 'ssdAmount': '80GB', 'ssdType': 'NVMe SSDs',
        'transferAmount': '4TB', 'link': 's-2vcpu-4gb-amd'}]

        result = extract_from_docean_js(self.docean_2)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
