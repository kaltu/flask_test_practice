import unittest
import requests


class TestingBase(unittest.TestCase):
    def setUp(self):
        self.api_url = 'http://127.0.0.1/user/signIn'

    def tearDown(self):
        pass


class CheckUserAndLogin(TestingBase):
    def test_get(self):
        response = requests.get(self.api_url)
        self.assertEqual(response.status_code, 405)

    def test_post(self):
        response = requests.post(self.api_url)
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        response = requests.post(self.api_url, data={
            'username': 'admin',
            'password': 'admin'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['msg'], 'login success')

    def wrong_credential(self, username: str, password: str):
        response = requests.post(self.api_url, data={
            'username': username,
            'password': password
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['msg'], 'login failed')

    def test_empty_credential(self):
        self.wrong_credential('', '')

    def test_unknown_account(self):
        self.wrong_credential('user', 'user')

    def test_wrong_password(self):
        self.wrong_credential('admin', '123')

    def test_exploit_sql(self):
        self.wrong_credential("';--", '')
        self.wrong_credential('admin', "' or ''='';--")

    def test_exploit_buffer_overflow(self):
        self.wrong_credential('admin', "\0" * 1024 * 1024 * 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
