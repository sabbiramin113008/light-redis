# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 28 Jul 2022
email: sabbiramin.cse11ruet@gmail.com, sabbir.amin@goava.com

"""
import json
import unittest
from core import Client

client = Client()


class ClientTest(unittest.TestCase):
    def test_client_set(self):
        key = "people:john"
        value = {
            "name": "John Doe",
            "age": 32
        }
        resp = client.set(key, value)
        print('Set Response:', resp)
        self.assertEqual(resp, 'OK')

    def test_client_get(self):
        key = "people:john"
        value = {
            "name": "John Doe",
            "age": 32
        }
        resp = client.get(key)
        print('GET response:', resp, type(resp))
        self.assertEqual(value, resp)

    def test_info(self):
        resp = client.info()
        print('Info Response:', resp)

    def test_lpush(self):
        key = "mma:legends"
        value = "GSP"
        resp = client.lpush(key, value)
        print(resp)

    def test_rpush(self):
        key = "mma:legends"
        value = "Tony Fergusonss"
        resp = client.rpush(key, value)
        print(resp)

    def test_lrange(self):
        key = "mma:legends"
        start = 0
        stop = 'inf'
        resp = client.lrange(key, start, stop)
        print(resp)


if __name__ == '__main__':
    unittest.main()
