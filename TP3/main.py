#! /usr/bin/env python3

import redis
from redis import RedisError
from http.server import BaseHTTPRequestHandler, HTTPServer
from flask import Flask, jsonify, request, redirect, url_for, make_response

r = redis.Redis(
    host='localhost',
    port=6379,
    password='')

# Clear the database, used for debugging, commented for security purposes
# r.flushdb()

app = Flask(__name__)

@app.route('/')
def index():
    if request.method == 'GET':
        return redirect(url_for('get_all'))

@app.route('/notes/', methods=['GET'])
def get_all():
    """Get all notes"""
    content = []
    alist = []
    content.append(r.lrange('lst_notes', 0, -1))
    content = str(content)
    items_nb = r.llen('lst_notes')
    for i in range(items_nb):
        alist.append(i)
    return jsonify(result = alist)

@app.route('/notes/', methods=['POST'])
def new_note():
    """Create a note"""
    r.rpush('lst_notes', request.data)
    return 'New note created !'

@app.route('/notes/<int:idnote>', methods=['GET'])
def get_note(idnote):
    """Get specific note"""
    return r.lindex('lst_notes', idnote)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
