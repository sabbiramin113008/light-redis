# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 29 Jul 2022
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com

"""

mlist = set()
mlist.add('meo')
mlist.discard('meo')
mlist.add('meao')

mlist.remove('meao')
mlist.add('meao')
aa = list(mlist)
ss = set(aa)

print(ss, type(ss))

print(mlist, len(mlist))
import json
import codecs

print(type(list(mlist)))
m = {
    'my:set': list(mlist)
}
with codecs.open('m.json', 'w', 'utf-8') as f:
    json.dump(m, f, ensure_ascii=False, indent=1)
