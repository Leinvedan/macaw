import unittest
from macaw.normalizer import normalize_plan


class NormalizerTestCase(unittest.TestCase):
    def setUp(self):
        self.expected = {
            "CPU / VCPU": "1",
            "MEMORY": "1GB",
            "STORAGE / SSD DISK": "25GB",
            "BANDWIDTH / TRANSFER" : "2.00TB",
            "PRICE [$/mo]": "$6.00",
        }
    def test_normalize_different_names(self):
        plan = {
            "CPU": "1",
            "Memory": "1GB",
            "Storage": "25GB",
            "Bandwidth": "2.00TB",
            "/mo": "$6.00",
            "/hr": "$0.009"
        }
        result = normalize_plan(plan)
        self.assertEqual(result, self.expected)


    def test_normalize_case_insensitive(self):
        plan = {
            "vCPU": "1",
            "MEMory": "1GB",
            "BANDWIDTH": "2.00TB",
            "StorAGE": "25GB",
            "/mo": "$6.00"
        }
        result = normalize_plan(plan)
        self.assertEqual(result, self.expected)
    
    def test_normalize_order_insensitive(self):
        plan = {
            "Memory": "1GB",
            "/hr": "$0.009",
            "Bandwidth": "2.00TB",
            "Storage": "25GB",
            "CPU": "1",
            "/mo": "$6.00",
        }
        result = normalize_plan(plan)
        self.assertEqual(result, self.expected)

if __name__ == '__main__':
    unittest.main()
