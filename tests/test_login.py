# tests/test_login.py
import unittest
import main
import json


class TestingBase(unittest.TestCase):
    def setUp(self):
        # self.app.test_request_context()
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        pass

    def login(self, username='', password=''):
        """
        Utility method for login
        :param username: str
        :param password: str
        :return: POST response
        """
        response = self.app.post('/user/signIn',
                                 follow_redirects=True,
                                 data={
                                     'username': username,
                                     'password': password
                                 })
        return response


class CheckUserAndLogin(TestingBase):
    def test_root(self):
        """
        Check root url, should be 302 found, not 200 ok
        """

        # Get root (redirect)
        resp = self.app.get('/')
        # Expecting 302 Found
        self.assertEqual(resp.status_code, 302)

    def test_index(self):
        """
        Check common /index, should be 404 not found
        """

        # Get index
        resp = self.app.get('/index')
        # Expecting 404 Not Found
        self.assertEqual(resp.status_code, 404)

    def test_login_page(self):
        """
        Check login page, should be 200 ok
        """
        resp = self.app.get('/login')
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        """
        Login with correct login credential
        """
        response = self.login(username='admin', password='admin')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], 'login success')

    def test_login_wrong(self):
        """
        Login with correct wrong credential
        """
        response = self.login(username='admin', password='123')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], 'login failed')

    def test_login_empty(self):
        """
        Login with blank username and password
        """
        response = self.login(username='', password='')
        
        # Expects 200 OK
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], 'login failed')

    def test_login_bad_request(self):
        """
        Test post request with empty form-data
        """
        response = self.app.post('/user/signIn')

        # Expects 400 Bad Request
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main(verbosity=2)
