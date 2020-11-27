# tests/test_api.py
import unittest
import requests


class TestingBase(unittest.TestCase):
    def setUp(self):
        self.api_url = 'http://127.0.0.1/user/signIn'
        self.correct_username = 'admin'
        self.correct_password = 'admin'

    def tearDown(self):
        pass


class CheckUserAndLogin(TestingBase):
    def test_get(self):
        """
        Sends not supported GET request
        Expects 405 Method Not Allowed
        :return:
        """
        response = requests.get(self.api_url)
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        """
        Sends empty POST request
        Expects 400 Bad Request
        :return:
        """
        response = requests.post(self.api_url)
        self.assertEqual(response.status_code, 400)

    def test_malformed_post(self):
        """
        Sends malformed POST request
        Expects 400 Bad Request
        """
        response = requests.post(self.api_url, data={
            'action': 'login'
        })
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        """
        Sends correct login credential with correct POST request
        Expects 200 OK for POST request
        Expects webpage showing "login success" message for login credential
        """
        # Correct POST request
        response = requests.post(self.api_url, data={
            'username': self.correct_username,
            'password': self.correct_password
        })
        # Expecting 200 OK
        self.assertEqual(response.status_code, 200)

        # Convert response byte stream to python dict
        data = response.json()
        self.assertEqual(data['msg'], 'login success')

    def wrong_credential(self, username: str, password: str):
        """
        Utility function for all incorrect login credential
        Sends incorrect login credential with correct POST request
        Expects 200 OK for POST request
        Expects webpage showing "login failed" message for login credential
        """
        # Correct POST request, login credential should be incorrect
        self.assertTrue(username != self.correct_username or password != self.correct_password)

        response = requests.post(self.api_url, data={
            'username': username,
            'password': password
        })
        # Expecting 200 OK
        self.assertEqual(response.status_code, 200)

        # Convert response byte stream to python dict
        data = response.json()
        self.assertEqual(data['msg'], 'login failed')

    def test_empty_credential(self):
        """
        login attempt with empty username and password
        """
        self.wrong_credential('', '')

    def test_unknown_account(self):
        """
        login attempt with non-existing user
        """
        self.wrong_credential('user', 'user')

    def test_wrong_password(self):
        """
        login attempt with wrong password
        """
        self.wrong_credential('admin', '123')

    def test_exploit_sql(self):
        """
        POST request with basic sql injection
        """
        self.wrong_credential("';--", '')
        self.wrong_credential('admin', "' or ''='';--")

    def test_exploit_buffer_overflow(self):
        """
        POST request with 2 mB data
        """
        self.wrong_credential('admin', '\0' * 1024 * 1024 * 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
