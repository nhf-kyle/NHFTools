#Version 23.01 [NOT STABLE, IN DEVELOPMENT] Utility Class for performing TCP operations to send/receive messages

import socket

class TCPServer:
    def __init__(self, network, handler):
        params = network['Input']
        addr = params['IP']
        port = int(params['Port'])
        timeout = float(params['Timeout'])
        self.handler     = handler
        self.buffer_size = 1024
        self.receiver    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receiver.settimeout(timeout)
        self.receiver.bind((addr, port))
        self.receiver.listen()

    #Receive a message from device. Send response if specified
    def receive(self, send_flag=True):
        while True:
            connection, addr = self.receiver.accept()
            data = connection.recv(self.buffer_size)
            if data:
                if send_flag:
                    self.handler(connection, data)
                break
        return data
        
class TCPClient:
    def __init__(self, network):
        self.transmitters = {}
        for item in network['Output']:
            #Extract connection details
            name = item['Name']
            self.transmitters[name] = {
                'addr' : item['IP'], 
                'port' : int(item['Port'])
            }
     
    #Send a message to a server/device. Wait for response if specified
    def send(self, name, message, response_flag = True, string_flag = True):
        data = None
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        params = self.transmitters[name]
        connection.connect((params['addr'], params['port']))
        #If string flag is false, send as raw bytes rather than as string
        if string_flag:
            message = message.encode('utf-8')
        connection.send(message)
        if response_flag:
            data = connection.recv(4096)
            data = data.decode("utf-8")
        connection.close()
        return data