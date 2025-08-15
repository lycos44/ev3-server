import json
import socket
import inspect
import logging
from threading import Thread

SIZE = 1024

logger = logging.getLogger(__name__)

class RPCServer:
    
    def __init__(self, host:str='0.0.0.0', port:int=8080) -> None:
        logger.debug('Init RPC server on {}:{}'.format(host, port))
        self.host = host
        self.port = port
        self.address = (host, port)
        self._methods = {}

    def help(self) -> None:
        print('REGISTERED METHODS:')
        for method in self._methods.items():
            print('\t',method)

    '''

        registerFunction: pass a method to register all its methods and attributes so they can be used by the client via rpcs
            Arguments:
            instance -> a class object
    '''
    def registerMethod(self, function) -> None:
        logger.debug('Registering method {}'.format(function.__name__))
        try:
            self._methods.update({function.__name__ : function})
        except:
            raise Exception('A non method object has been passed into RPCServer.registerMethod(self, function)')

    '''
        registerInstance: pass a instance of a class to register all its methods and attributes so they can be used by the client via rpcs
            Arguments:
            instance -> a class object
    '''
    def registerInstance(self, instance=None) -> None:
        logger.debug('Registering instance {}'.format(instance))
        try:
            # Regestring the instance's methods
            for functionName, function in inspect.getmembers(instance, predicate=inspect.ismethod):
                if not functionName.startswith('__'):
                    self._methods.update({functionName: function})
        except:
            raise Exception('A non class object has been passed into RPCServer.registerInstance(self, instance)')

    '''
        handle: pass client connection and it's address to perform requests between client and server (recorded fucntions or) 
        Arguments:
        client -> 
    '''
    def __handle__(self, client:socket.socket, address:tuple):
        logger.info('Handling request from {}'.format(address[0], address[1]))
        while True:
            try:
                functionName, args, kwargs = json.loads(client.recv(SIZE).decode())
            except: 
                break
            # Showing request Type
            logger.info('Request {}({})'.format(functionName, ', '.join(map(str, args))))
            
            try:
                response = self._methods[functionName](*args, **kwargs)
            except Exception as e:
                # Send back exeption if function called by client is not registred 
                client.sendall(json.dumps(str(e)).encode())
            else:
                client.sendall(json.dumps(response).encode())


        logger.info('Client {}:{} disconnected.'.format(address[0], address[1]))
        # Closing client connection
        client.close()
    
    def run(self) -> None:
        logger.info('Starting RPC server on {}:{}'.format(self.host, self.port))
        # Creating a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(self.address)
            sock.listen()

            logger.info('Server is running on {}:{}'.format(self.host, self.port))
            logger.info('Waiting for connections...')
            
            while True:
                try:
                    client, address = sock.accept()
                    logger.info('Connection from {}:{}'.format(address[0], address[1]))
                    
                    Thread(target=self.__handle__, args=[client, address]).start()

                except KeyboardInterrupt:
                    logger.info('Server is shutting down...')
                    sock.close()
                    logger.info('Server on {}:{} is closed.'.format(self.host, self.port))
                    break
