# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 25 Jul 2022
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""
import json

import codecs


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = dict()

    def init_database(self):
        with codecs.open(self.db_file, 'w', 'utf-8') as f:
            json.dumps(self.db, ensure_ascii=False, indent=1)


