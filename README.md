## Light-Redis

`Light-Redis` is a Redis Like Data Structure Database (Server and Client) Based on `Python Dict` and `Flask`

## Current Features:
1. A Server for interacting incoming Client Requests.
2. A Python Client for interacting with the Server and the database.
3. A Scheduler that takes snapshot of the database and stores it to disk.
4. A CLI with Completion Help. 
5. Redis Like Commands ( Currently, there are few, but I will eventually mimic all ISA :D )

## Starting the `server` from the CLI

When the `server` is started it initially looks for previous snapshots in the directory it is
started. If found it loads the data in the memory and starts the `waitress` based server which
actually runs with a `Flask` app behind. As it is `http` based server, clients need to connect via
http protocol, to ease the transition a build in `Client` is also provided to use it directly
into the python code.

To start the server, just run

``` python
python lightredis.py --host <host> --port <port> --dump_file_name <dump_database_file_name> --time_to_check_snapshot <time_to_check_snapshot>

```

to set it with options, or simply

```python
python
lightredis.py
```

## Interacting the Database with `Python Client`

To start manipulating data in from the python code, start it with initiating the client.

```python
from lightredis import Client

client = Client(base_url='http://localhost:5055')

# set the data
key = "people:john"
value = {
    "name": "John Doe",
    "age": 32
}
resp = client.set(key, value)
print('Set Response:', resp)

# Get the Data
key = "people:john"
value = {
    "name": "John Doe",
    "age": 32
}
resp = client.get(key)
print('GET response:', resp)

```

Internally, the client calls the `http: endpoint` with `POST` and does all the heavy-lifting.

## Interacting the Database with `requests`

As the database action APIs are exposed over the the `HTTP`, the database
can be manipulated with any `http-client`. `requests` is the most commonly used one
in python world, this also can be used. Let's look at the example.

```python
import requests

url = "http://localhost:5055/"

payload = {
    "cmd": "set",
    "key": "mma:tony",
    "value": {
        "name": "Tony Ferguson",
        "stance": "Orthodox",
        "division": "Lightweight"
    }
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

So, literally, this is the same example, that can be done with the `python-client`.

## A toy Client `CLI` like `redis-cli`.

To start the `cli` just run,

```python
python
cli.py - -url < url > 
```

or simply

```python
python
cli.py
```

This will start a `repl` like toy shell that would use the
`python client` for the interaction with the database. As a typing 
completion support, `prompt-toolkit` is used. Let's have a look. 

```bash
nemo@nautilus:~/Documents/kontainer/personal/pyproject/light-redis$ python cli.py 
>>set animal:name horse
OK
>>get animal:name
horse
>>sadd animal:world tiger
OK
>>sadd animal:world lion
OK
>>smembers animal:world
['lion', 'tiger']
>>info
{'db_file_name': 'db.json', 'keys': ['name', 'person:name', 'os', 'animal:name', 'animal:world'], 'keys_count': 5, 'last_db_snapshot_write': 1659103181, 'writable_row': 3}
>>save
OK
>>                                                                                                                                                                                   
XX-- Shutting Down --XX
nemo@nautilus:~/Documents/kontainer/personal/pyproject/light-redis$ exit


```

Have a look at the asciinema cast here ![demo] (https://asciinema.org/a/x05Ji9igVzZX3QhphPVqFPmeI)

