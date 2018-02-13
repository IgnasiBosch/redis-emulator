# REDIS-EMULATOR

In order to be able to test and debug services which depend or are based in redis pubsub, here some scripts that could be useful:

## SERVER
`$ python redis_emulator_server.py -h` 
Emulates a redis server and emit all PUBLISH and MESSAGE payloads types 


## SUBSCRIBER
`$ python redis_emulator_publisher.py -h`  
Subscribes to a redis pubsub channel


## PUBLISHER
`$ python redis_emulator_publisher.py -h`  
Publish to a redis pubsub channel  

## MESSAGE (PUBLISHER EMULATOR)
`$ python redis_emulator_message.py -h`  
Emulates a redis publishing to pubsub channel
