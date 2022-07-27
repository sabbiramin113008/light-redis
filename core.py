# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 27 Jul 2022
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
import codecs
import json

from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
from waitress import serve

OK = 'OK'
ERROR = 'ERROR'
NOT_A_VALID_COMMAND = 'NOT_A_VALID_COMMAND'

DUMP_FILE_NAME = 'db.json'


def dump_database(db):
    print('db:', db)
    try:
        with codecs.open('db.json', 'w', 'utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('Error:', str(e))


def load_database(db_file_name):
    db = {}
    try:
        with codecs.open(db_file_name, 'r', 'utf-8') as f:
            model = json.load(f)
        return model
    except Exception as e:
        print('Error: No Database Snapshot:', str(e))
        return db


class Server:
    def __init__(self, host='localhost', dump_file_name=DUMP_FILE_NAME, port=5055, debug=True):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.db_file_name = dump_file_name
        self.db = load_database(self.db_file_name)

        self.write_count = 0
        self.debug = debug
        self.scheduler = APScheduler()
        self.scheduler.api_enabled = True
        self.scheduler.init_app(self.app)
        self.scheduler.start()

        def parse_request(request, arg):
            data = request.get_json()
            return data.get(arg, None)

        def _set(request):
            cmd, key, val = parse_request(request, 'cmd'), parse_request(request, 'key'), parse_request(request,
                                                                                                        'value')
            if key and val:
                self.db[key] = {
                    'val': val,
                    'cmd': cmd
                }
                self.write_count += 1
                return OK
            else:
                return ERROR

        def _get(request):
            key = parse_request(request, 'key')
            try:
                return self.db[key]['val']
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
            @self.scheduler.task('interval', id='backup_job_1', seconds=10, misfire_grace_time=900)
            def task_dump_after_10_seconds():
                print('write_count:', self.write_count)
                if self.write_count > 10:
                    dump_database(db=self.db)
                    print('snapshots: Db Snapshot Taken')
                    self.write_count = 0
                else:
                    print('snapshots: Not Enough Write Count')

            serve(self.app, port=self.port, host=self.host, max_request_body_size=1073741824 * 10,
                  inbuf_overflow=1073741824 * 10)


if __name__ == '__main__':
    server = Server()
    server.run(multi=True)
