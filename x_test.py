# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 29 Jul 2022
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""

import requests

url = "http://localhost:5055/"

payload = {
    "cmd": "get",
    "key": "hello"
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.json())