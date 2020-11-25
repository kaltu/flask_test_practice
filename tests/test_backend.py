import unittest
from main import check_credential


class TestingBase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class CheckBackend(TestingBase):
    def test_credential(self):
        self.assertTrue(check_credential('admin', 'admin'))

    def test_wrong_credential(self):
        self.assertFalse(check_credential('admin', '123'))

    def test_exploit_sql(self):
        self.assertFalse(check_credential('admin', "' or ''='';--"))

    def test_buffer_overflow(self):
        self.assertFalse(check_credential('admin', '\0' * 1024 * 1024 * 2))


if __name__ == '__main__':
    unittest.main(verbosity=2)
