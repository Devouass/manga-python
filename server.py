#!/usr/bin/env python
import os
import sys
from flask import Flask, abort, request, jsonify, g, url_for, send_from_directory, redirect
from flask.ext.login import LoginManager, login_required, login_user, logout_user
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from serverUtils import DbConnection, User

app = Flask("manga_server", static_folder='static')
app.secret_key = 'mySecretKeyForMyApp'
login_manager = LoginManager()
login_manager.init_app(app)
db = DbConnection()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_LIB = os.path.join(APP_ROOT, 'htmlLibrary')

def _log(message):
    sys.stdout.write(message)
    sys.stdout.write('\n')
    sys.stdout.flush()

@app.errorhandler(500)
def internal_error(error):
    _log("in internal error")
    _log("error is {}".format(error))

@login_manager.user_loader
def load_user_id(user_id):
    _log("try to load user with id {}".format(user_id))
    user = User.get(user_id)
    _log("user_loader : user is {}".format(user))
    return user

@login_manager.unauthorized_handler
def unauthorized_access():
    _log("unauthorized access")
    return redirect(url_for("index"))

@app.route('/images/<path:filename>')
def serve_static_images(filename):
    return send_from_directory('static/images', filename)

@app.route('/css/<path:filename>')
def serve_static_css(filename):
    return send_from_directory('static/css', filename)

@app.route('/lib/<path:filename>')
def serve_static_lib(filename):
    return send_from_directory('static/lib', filename)

@app.route('/script/<path:filename>')
def serve_static_script(filename):
    return send_from_directory('static/script', filename)

@app.route("/login", methods=["GET","POST"])
def check_login():
    if request.method == 'GET':
        return redirect(url_for("index"))
    if not request.json:
        abort(400)
    user = request.json['login']
    passwd = request.json['pwd']
    _log('user is {} and pwd is  {}'.format(user, passwd))
    u = User.get(user)
    u.authenticated = True
    _log("try to log user")
    login_user(u, remember=False)
    _log("user logged")
    return jsonify(user = u.id)

@app.route('/')
def index():
    _log("root asked")
    return send_from_directory('htmlpages', 'index.html')

@app.route('/logout')
def logout():
    _log("logout user")
    u = User.get("jerem")
    u.authenticated = False
    logout_user()
    return redirect(url_for("index"))

@app.route("/view", methods=["GET"])
@login_required
def get_routes():
    _log("view asked")
    return send_from_directory('htmlpages', 'viewer.html')


if __name__ == '__main__':
    db.connect()
    #user = User("jerem")
    #user.hash_password("Admin1&&")
    #db.saveUser(user.id, user.password_hash)
    User.user = db.getUser("jerem")
    app.run(host='127.0.0.1', port=8082, debug=True)
