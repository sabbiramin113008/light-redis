# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 27 Jul 2022
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""

from flask import Flask, request


class Server:
    def __init__(self, host='localhost', port=5055, debug=True):
        self.app = Flask(__name__)
        self.db = {}
        self.host = host
        self.port = port
        self.debug = debug

        def _set(*args):
            for arg in args:
                print(arg)
            key = args[0]
            val = args[1]
            self.db[key] = val
            return 'OK'

        def _get(*args):
            key = args[0]
            try:
                return self.db[key]
            except Exception as e:
                return 'None'

        self.command_handler = {'set': _set, 'get': _get}

        def handler():
            data = request.get_json()
            cmd, key, value = data.get('cmd'), data.get('key'), data.get('value')
            resp = self.command_handler[cmd](key, value)
            print('resp:', resp)
            return resp

        self.app.add_url_rule("/", view_func=handler, methods=['POST'])

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)


if __name__ == '__main__':
    server = Server()
    server.run()

