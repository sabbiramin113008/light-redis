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

    def test_set_simple(self):
        key = 'hello:world'
        value = "WOW"
        print(client.set(key, value))

    def test_get_simple(self):
        key = 'hello:world'
        value = "WOW"
        print(client.get(key))


if __name__ == '__main__':
    unittest.main()
