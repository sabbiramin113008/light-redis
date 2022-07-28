## Light-Redis
A Redis Like Data Structure (Server and Client) Based on Python Dict and Flask

## Clients
1. For `set` the client converts the value via `json.dumps`
   to keep it as string.
2. Also, loads the data back to data by calling the `json.loads`.