#!/usr/bin/env python
import os
from flask import Flask, abort, request, jsonify, g, url_for, send_from_directory
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask("manga_server")


@app.route('/')
def root():
    #return app.send_static_file('htmlpages/index.html')
    return send_from_directory('htmlpages', 'index.html')

@app.route("/test", methods=["GET"])
def test():
    return jsonify({'username': 'jerem'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8082, debug=True)
