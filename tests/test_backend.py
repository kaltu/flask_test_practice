# tests/test_backend.py
import unittest
from main import check_credential

from distutils.version import StrictVersion
from flask_cors import __version__ as cors_version


class TestingBase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class CheckBackend(TestingBase):
    def test_credential(self):
        """
        correct credentials
        """
        self.assertTrue(check_credential('admin', 'admin'))

    def test_empty_credential(self):
        """
        empty credential
        """
        self.assertFalse(check_credential('', ''))

    def test_unknown_user(self):
        """
        unknown user
        """
        self.assertFalse(check_credential('user', 'admin'))

    def test_wrong_credential(self):
        """
        wrong password
        """
        self.assertFalse(check_credential('admin', '123'))

    def test_exploit_sql(self):
        """
        basic sql injection
        """
        self.assertFalse(check_credential('admin', "' or ''='';--"))

    def test_buffer_overflow(self):
        """
        2 mB long data
        """
        self.assertFalse(check_credential('admin', '\0' * 1024 * 1024 * 2))

    # TODO
    def test_CVE_2020_25032(self):
        """
        We're using flask-cors, it has known vulnerability CVE-2020-25032 before 3.0.9 (exclusive)
        Current latest version of flask-cors is 3.0.9, in any event we need to rollback to older version,
        this test shall fail.
        """
        self.assertGreaterEqual(StrictVersion(cors_version), StrictVersion('3.0.9'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
