from flask import Flask, render_template, request, url_for, redirect, jsonify, abort
from flask_restful import Api
import requests

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return redirect(url_for('login_page'))


def check_credential(username, password):
    # for simplicity, plain-text only
    # otherwise, use flask-login
    return username == 'admin' and password == 'admin'


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return render_template('login.html')


@app.route('/user/signIn', methods=['POST'])
def login_api():
    if request.method == 'POST':
        if not request.form:
            return abort(400)
        # if request.form['username'] == 'admin' and request.form['password'] == 'admin':
        if check_credential(request.form['username'], request.form['password']):
            return jsonify({'msg': 'login success'})
        else:
            return jsonify({'msg': 'login failed'})


@app.cli.command('test')
def test():
    import unittest
    import sys

    try:
        tests = unittest.TestLoader().discover("tests")
        result = unittest.TextTestRunner(verbosity=2).run(tests)
    except requests.ConnectionError as e:
        print(e)
        print('Server Offline')
        sys.exit(1)

    if result.errors or result.failures:
        sys.exit(1)
