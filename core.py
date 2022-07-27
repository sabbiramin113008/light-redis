# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 27 Jul 2022
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""

from flask import Flask, request, jsonify
from waitress import serve

OK = 'OK'
ERROR = 'ERROR'
NOT_A_VALID_COMMAND = 'NOT_A_VALID_COMMAND'


class Server:
    def __init__(self, host='localhost', port=5055, debug=True):
        self.app = Flask(__name__)
        self.db = {}
        self.host = host
        self.port = port
        self.debug = debug

        def parse_request(request, arg):
            data = request.get_json()
            return data.get(arg, None)

        def _set(request):
            cmd, key, val = parse_request(request, 'cmd'), parse_request(request, 'key'), parse_request(request,
                                                                                                        'value')
            if key and val:
                self.db[key] = val
                return OK
            else:
                return ERROR

        def _get(request):
            key = parse_request(request, 'key')
            try:
                return self.db[key]
            except Exception as e:
                print('Error:', str(e))
                return ERROR

        self.command_handler = {'set': _set, 'get': _get}

        def handler():
            cmd = parse_request(request, 'cmd')
            try:
                resp = self.command_handler[cmd](request)
                print('resp:', resp)
                return resp
            except KeyError:
                return NOT_A_VALID_COMMAND

        self.app.add_url_rule("/", view_func=handler, methods=['POST'])

    def run(self, multi=False):
        if not multi:
            self.app.run(host=self.host, port=self.port, debug=self.debug)
        else:
            serve(self.app, port=self.port, host=self.host, max_request_body_size=1073741824 * 10,
                  inbuf_overflow=1073741824 * 10)


if __name__ == '__main__':
    server = Server()
    server.run(multi=True)
