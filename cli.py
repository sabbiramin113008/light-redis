# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 29 Jul 2022
email: sabbiramin.cse11ruet@gmail.com, sabbir.amin@goava.com

"""
import optparse
from lightredis import Client
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter

command_set = {}
command_set['set'] = {'key value': None}
command_set['get'] = {'key': None}
command_set['info'] = {'Returns the Information of the System'}
command_set['sadd'] = {'key value': None}
command_set['save'] = {'Immediately Schedules to take a DB Snapshot': None}
command_set['smembers'] = {'key': None}

completer = NestedCompleter.from_nested_dict(data=command_set)


def sanitize_index(index: int, tokens: list):
    try:
        return tokens[index]
    except IndexError:
        return None


class Mapper(dict):
    def __init__(self, key_map: dict):
        for key, val in key_map.items():
            self.__dict__[key] = val


def reverse_parse(text: str, tokens: list):
    texts = text.split()
    maps = {}
    for index, token in enumerate(tokens):
        maps[token] = sanitize_index(index, texts)
    mapper = Mapper(maps)
    return mapper


def get_options():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', dest='url', default='http://localhost:5055', help='Set Base URL')
    return parser


def cmd_execute(client, text):
    cmd = text.split(' ')[0]
    if cmd == 'set':
        maps = reverse_parse(text, ['cmd', 'key', 'value'])
        return client.set(key=maps.key, value=maps.value)
    elif cmd == 'get':
        maps = reverse_parse(text, ['cmd', 'key'])
        return client.get(key=maps.key)
    elif cmd == 'info':
        return client.info()
    elif cmd == 'sadd':
        maps = reverse_parse(text, ['cmd', 'key', 'value'])
        return client.sadd(key=maps.key, value=maps.value)
    elif cmd == 'save':
        return client.save()
    elif cmd == 'smembers':
        maps = reverse_parse(text, ['cmd', 'key'])
        return client.smembers(key=maps.key)
    else:
        return "INVALID_COMMAND_KEY"


def cli(base_url: str):
    client = Client(base_url=base_url)
    try:
        while True:
            text = prompt('>>', completer=completer)
            resp = cmd_execute(client, text)
            print(resp)
    except KeyboardInterrupt:
        print("XX-- Shutting Down --XX")


if __name__ == '__main__':
    options, args = get_options().parse_args()
    cli(base_url=options.url)
