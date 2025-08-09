#!/usr/bin/env python3
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger.info('Started')
    
def add(a, b):
    return a+b

def sub(a, b):
    return a-b

from rpc import RPCServer

server = RPCServer()

server.registerMethod(add)
server.registerMethod(sub)

server.run()
logger.info('Finished')
