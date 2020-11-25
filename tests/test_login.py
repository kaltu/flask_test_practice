import unittest
import main
import requests
import json


class TestingBase(unittest.TestCase):
    def setUp(self):
        # self.app.test_request_context()
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()
        self.username = ''
        self.password = ''

    def tearDown(self):
        pass

    def login(self):
        response = self.app.post('/user/signIn',
                                 follow_redirects=True,
                                 data={
                                     'username': self.username,
                                     'password': self.password
                                 })
        return response


class CheckUserAndLogin(TestingBase):
    def test_root(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 302)

    def test_index(self):
        resp = self.app.get('/index')
        self.assertEqual(resp.status_code, 404)

    def test_login_page(self):
        resp = self.app.get('/login')
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        self.username = 'admin'
        self.password = 'admin'
        response = self.login()
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], 'login success')

    def test_login_wrong(self):
        self.username = 'admin'
        self.password = '123'
        response = self.login()
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], 'login failed')

    def test_login_empty(self):
        self.username = ''
        self.password = ''
        response = self.login()
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['msg'], 'login failed')

    def test_login_bad_request(self):
        response = self.app.post('/user/signIn')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main(verbosity=2)
