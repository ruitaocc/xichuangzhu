import unittest
import xichuangzhu as xcz

class XczTestCase(unittest.TestCase):

    def setUp(self):
        xcz.app.config['TESTING'] = True
        self.app = xcz.app.test_client()

    def test_a(self):
        assert True

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()