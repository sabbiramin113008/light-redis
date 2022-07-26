## Light-Redis
A Redis Data Structure Based on Python Dict. 

## Options
1. File Based Database Storage accessed based on Queue.
2. Server-Client model based on simple http server and multiple client. Here database lives in the server process.
3. Server-Client using socket. 

## File Based Database Storage - concerns, thoughts and points. 
1. Lock the resource.
2. Command insert into the Queue.
3. Introduce `timelimit` for allowing each request equal treatment based on predefined time slot.
4. Global monitor for executing commands in-parallel.
5. How do we avoid Race conditions? Resource locking?