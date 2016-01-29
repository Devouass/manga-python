#!/usr/bin/env python
import os
import sys
from flask import Flask, abort, request, jsonify, g, url_for, send_from_directory, redirect
from flask.ext.login import LoginManager, login_required, login_user, logout_user
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
def load_user_by_id(user_id):
    _log("try to load user with id {}".format(user_id))
    user = db.getUser(user_id)
    _log("user_loader : user is {}".format(user))
    return user

@login_manager.unauthorized_handler
def unauthorized_access():
    _log("unauthorized access")
    return redirect(url_for("index")), 401

@app.route('/images/<path:filename>')
def serve_static_images(filename):
    return send_from_directory('static/images', filename)

@app.route('/css/<path:filename>')
def serve_static_css(filename):
    return send_from_directory('static/css', filename)

@app.route('/lib/<path:filename>')
def serve_static_lib(filename):
    return send_from_directory('static/lib', filename)

@app.route('/www/<path:filename>')
def serve_static_script(filename):
    return send_from_directory('static/', filename)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'GET':
        #return send_from_directory('htmlpages', 'index.html')
        return redirect(url_for("login")), 401
    if not request.json:
        abort(400)
    status = 401
    login = request.json['login']
    passwd = request.json['pwd']
    user = db.getUser(login)
    if user is not None:
        if user.verify_password(passwd):
            user.authenticated = True
            login_user(user, remember=False)
            status = 200
            return jsonify(name = user.id), status
    return '', status

@app.route('/')
def index():
    _log("root asked")
    return send_from_directory('static', 'index.html')

@app.route('/logout')
def logout():
    _log("logout user")
    logout_user()
    return redirect(url_for("index"))

@app.route("/mangas", methods=["GET"])
@login_required
def get_mangas():
    return jsonify(\
        {\
        'mangas' : [\
        {'name':'fairy tail','start' : 200, 'stop' : 210, 'image_url':'/images/fairy_tail_natsu.png'},\
        {'name':'one piece', 'start' : 100, 'stop' : 105, 'image_url':'/images/one_piece_lutfy.png'}\
        ]\
        }), 200

if __name__ == '__main__':
    db.connect()
    #user = User("toto")
    #user.hash_password("toto")
    #db.saveUser(user)
    app.run(host='127.0.0.1', port=8082, debug=True)
