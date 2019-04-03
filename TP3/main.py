#! /usr/bin/env python3

import redis, requests, http, sys, flask
from http.server import BaseHTTPRequestHandler, HTTPServer

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
      self.send_response(200)

      self.send_header('Content-type','text/html')
      self.end_headers()

      message = "Here are the notes:"
      self.wfile.write(bytes(message, "utf8"))
      return

  def do_POST(self):
      pass

def run():
  print('starting server...')

  server_address = ("127.0.0.1", 8080)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

run()

r = redis.Redis(
    host='localhost',
    port=6379,
    password='')

r.set('4', 'note_victor')
value = r.get('4')
print(value)
