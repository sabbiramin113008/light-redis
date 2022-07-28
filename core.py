# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 27 Jul 2022
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
import calendar
import codecs
import json
import time

from typing import Any

import requests
from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
from waitress import serve

OK = 'OK'
ERROR = 'ERROR'
NOT_A_VALID_COMMAND = 'NOT_A_VALID_COMMAND'
TIME_DELTA_TO_FORCE_SNAPSHOT = 300
DUMP_FILE_NAME = 'db.json'


def dump_database(db):
    print('db:', db)
    try:
        with codecs.open('db.json', 'w', 'utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('Error:', str(e))


def get_current_time():
    return calendar.timegm(time.gmtime())


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
        self.last_snapshot_time = 0
        self.debug = debug
        self.scheduler = APScheduler()
        self.scheduler.api_enabled = True
        self.scheduler.init_app(self.app)
        self.scheduler.start()

        def parse_request(request, arg):
            data = request.get_json()
            return data.get(arg, None)

        def _set(request):
            cmd, key, val = parse_request(request, 'cmd'), \
                            parse_request(request, 'key'), \
                            parse_request(request, 'value')
            if key and val:
                self.db[key] = {
                    'val': val,
                    'cmd': cmd,
                    'created': get_current_time()
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

        def _info(request):
            resp = {
                'keys_count': len(self.db.keys()),
                'keys': list(self.db.keys()),
                'writable_row': self.write_count,
                'db_file_name': self.db_file_name,
                'last_db_snapshot_write': self.last_snapshot_time,
            }
            return json.dumps(resp)

        def _lpush(request):
            cmd, key, val = parse_request(request, 'cmd'), \
                            parse_request(request, 'key'), \
                            parse_request(request, 'value')
            if key and val:
                try:
                    # find if the key exists and cmd valid
                    if self.db[key] and isinstance(self.db[key]['val'], list):
                        pre_list: list = self.db[key]['val']
                        pre_list.insert(0, val)
                        new_list = list(set(pre_list))
                        self.db[key] = {
                            'val': new_list,
                            'cmd': cmd,
                            'key': key,
                            'created': get_current_time()
                        }
                        self.write_count += 1
                        return str(len(new_list))
                except Exception as e:
                    print('error:', str(e))
                    new_list = [val]
                    self.db[key] = {
                        'val': new_list,
                        'cmd': cmd,
                        'key': key,
                        'created': get_current_time()
                    }
                    self.write_count += 1
                    self.last_snapshot_time = get_current_time()
                    return str(len(new_list))
            return ERROR

        def _rpush(request):
            cmd, key, val = parse_request(request, 'cmd'), \
                            parse_request(request, 'key'), \
                            parse_request(request, 'value')
            if key and val:
                try:
                    # find if the key exists and cmd valid
                    if self.db[key] and isinstance(self.db[key]['val'], list):
                        pre_list: list = self.db[key]['val']
                        pre_list.append(val)
                        new_list = list(set(pre_list))
                        self.db[key] = {
                            'val': new_list,
                            'cmd': cmd,
                            'key': key,
                            'created': get_current_time()
                        }
                        self.write_count += 1
                        return str(len(new_list))
                except Exception as e:
                    print('error:', str(e))
                    new_list = [val]
                    self.db[key] = {
                        'val': new_list,
                        'cmd': cmd,
                        'key': key,
                        'created': get_current_time()
                    }
                    self.write_count += 1
                    return str(len(new_list))
            return ERROR

        def _lrange(request):
            cmd, key, start, stop = parse_request(request, 'cmd'), \
                                    parse_request(request, 'key'), \
                                    parse_request(request, 'start'), \
                                    parse_request(request, 'stop')

            if key and start and stop:
                try:
                    if self.db[key] and isinstance(self.db[key]['val'], list):
                        pre_list: list = self.db[key]['val']
                        if stop == 'inf':

                            tmp_list = pre_list[int(start):]
                        else:
                            tmp_list = pre_list[int(start):int(stop)]
                        print('tmp list:', tmp_list)
                        return json.dumps(tmp_list)
                    else:
                        return ERROR
                except Exception as e:
                    print('Error:', str(e))
                    return ERROR
            return ERROR

        self.command_handler = {
            'set': _set,
            'get': _get,
            'info': _info,

            'lpush': _lpush,
            'rpush': _rpush,
            'lrange': _lrange

        }

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
                    self.last_snapshot_time = get_current_time()
                elif self.write_count and get_current_time() - self.last_snapshot_time > TIME_DELTA_TO_FORCE_SNAPSHOT:
                    dump_database(db=self.db)
                    print('snapshots: Force Db Snapshot Taken')
                    self.write_count = 0
                    self.last_snapshot_time = get_current_time()
                else:
                    print('snapshots: Not Enough Write Count')

            serve(self.app, port=self.port, host=self.host, max_request_body_size=1073741824 * 10,
                  inbuf_overflow=1073741824 * 10)


class Client:
    def __init__(self, base_url='http://localhost:5055'):
        self.base_url = base_url

    def call(self, body):
        headers = {"Content-Type": "application/json"}
        resp = 'ERROR'
        try:
            resp = requests.post(url=self.base_url,
                                 headers=headers,
                                 json=body)
            return resp.text
        except Exception as e:
            print('Error Calling Base:', str(e))
        return resp

    def set(self, key: str, value: Any):
        body = {
            "cmd": "set",
            "key": key,
            "value": json.dumps(value)
        }
        return self.call(body)

    def get(self, key: str):
        body = {
            "cmd": "get",
            "key": key,
        }
        resp = self.call(body)
        if resp == 'ERROR':
            return ERROR
        return json.loads(resp)

    def info(self):
        body = {"cmd": "info"}
        resp = self.call(body)
        return json.loads(resp)

    def lpush(self, key: str, value: str):
        body = {
            "cmd": "lpush",
            "key": key,
            "value": value
        }
        return self.call(body)

    def rpush(self, key: str, value: str):
        body = {
            "cmd": "rpush",
            "key": key,
            "value": value
        }
        return self.call(body)

    def lrange(self, key: str, start: int, stop: str):
        body = {"cmd": "lrange", "key": key, "start": start, "stop": stop}
        resp = self.call(body)
        return ERROR if resp == ERROR else resp


if __name__ == '__main__':
    server = Server()
    server.run(multi=True)
