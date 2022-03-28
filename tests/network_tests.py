import unittest
from macaw.network import _get_file_type


class NetworkTestCase(unittest.TestCase):
    def test_get_correct_extension(self):
        url_1 = 'https://www.vultr.com'
        url_2 = '/_next/static/chunks/pages/pricing-1a7cdb1f9a255535.js'
        result_1 = _get_file_type(url_1)
        result_2 = _get_file_type(url_2)
        self.assertEqual(result_1, 'html')
        self.assertEqual(result_2, 'js')

if __name__ == '__main__':
    unittest.main()
