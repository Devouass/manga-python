#!/usr/bin/env python
import os
import sys
from flask import Flask, abort, request, jsonify, g, url_for, send_from_directory, redirect
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask("manga_server", static_folder='static')

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

@app.route('/lib/<path:filename>')
def serve_static_lib(filename):
    return send_from_directory('static/lib', filename)

@app.route('/script/<path:filename>')
def serve_static_script(filename):
    return send_from_directory('static/script', filename)

@app.route("/test", methods=["GET"])
def test():
    return jsonify({'username': 'jerem'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8082, debug=True)
