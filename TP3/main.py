#! /usr/bin/env python3

import redis, http, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from flask import Flask, jsonify, request, redirect, url_for, make_response

r = redis.Redis(
    host='localhost',
    port=6379,
    password='')

# Clear the database
r.flushdb()

# Debug insertions
r.lpush('lst_notes', 'note_victor')
r.lpush('lst_notes', 'note_david')
r.lpush('lst_notes', 'note_pataya')

app = Flask(__name__)

@app.route('/')
def index():
    if request.method == 'GET':
        return redirect(url_for('get_all'))

@app.route('/notes/', methods=['GET'])
def get_all():
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
    r.rpush('lst_notes', request.data)
    return 'ok'

@app.route('/notes/<int:idnote>', methods=['GET'])
def get_note(idnote):
    return r.lindex('lst_notes', idnote)

@app.route('/notes/idnote', methods=['DELETE'])
def delete_note(idnote):
    r.lrem('lst_notes', 0, idnote)
    return 'ok'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
