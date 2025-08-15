#!/usr/bin/env python3
import logging
import logging.config
import os
from rpc import RPCServer


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(module)s : %(lineno)d - %(message)s',
                    handlers=[logging.FileHandler("../logs/ev3-server.log"),
                              logging.StreamHandler()])

# create logger
logger = logging.getLogger('ev3-server')
    
def add(a, b):
    return a+b

def sub(a, b):
    return a-b

def main():
    server = RPCServer()

    server.registerMethod(add)
    server.registerMethod(sub)

    server.run()

if __name__ == '__main__':
    main()  
