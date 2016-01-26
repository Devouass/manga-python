#!/usr/bin/env python
import os
import sys
from flask import Flask, abort, request, jsonify, g, url_for, send_from_directory, redirect
from flask_httpauth  import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from serverUtils import DbConnection, User

app = Flask("manga_server", static_folder='static')
auth = HTTPBasicAuth()
db = DbConnection()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_LIB = os.path.join(APP_ROOT, 'htmlLibrary')

def _log(message):
    sys.stdout.write(message)
    sys.stdout.write('\n')
    sys.stdout.flush()

@app.route('/')
def root():
    _log("root asked")
    return send_from_directory('htmlpages', 'index.html')

@app.route('/css/<path:filename>')
def ser_static_css(filename):
    return send_from_directory('static/css', filename)

@auth.error_handler
def auth_error():
    return "&lt;h1&gt;Access Denied&lt;/h1&gt;"

@app.route('/lib/<path:filename>')
def serve_static_lib(filename):
    return send_from_directory('static/lib', filename)

@app.route('/script/<path:filename>')
def serve_static_script(filename):
    return send_from_directory('static/script', filename)

@app.route("/login", methods=["POST"])
def check_login():
    if not request.json:
        abort(400)
    return jsonify({}), 201

@app.route("/view", methods=["GET"])
@auth.login_required
def get_routes():
    return jsonify({}), 201

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        _log("no user, username_or_token is {} and psswd is {}".format(username_or_token, password))
        # try to authenticate with username/password
        user = db.getUser(username_or_token)
        _log("user is {}".format(user))
        if not user or not user.verify_password(password):
            return False
    return True

def createUser(name, password):
    user = User(name)
    user.hash_password(password)
    db.saveUser(user.id, user.password_hash)

if __name__ == '__main__':
    db.connect()
    createUser("jerem", "Admin1&+")
    app.run(host='127.0.0.1', port=8082, debug=True)
