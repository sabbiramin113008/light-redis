# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 29 Jul 2022
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
from cli import reverse_parse


def check():
    text = "set name value"
    mm = reverse_parse(text, ['cmd', 'key', 'value'])
    print(mm)


if __name__ == '__main__':
    check()
