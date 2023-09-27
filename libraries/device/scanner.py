#Version 23.08 Library to manipulate Keyence SR Series Barcode Readers (for triggering inspection and reading results)

import time
import socket

class Scanner:
    def __init__(self, config):
        self.addr    = config['IP']
        self.port    = config['Port']
        self.trigger = config['Trigger']
        self.output  = config['Result']
           
    #Trigger scanner and acquire barcode result
    def read(self):
        done = False
        while not done:
            #Send Trigger to Scanner
            message    = 'LON\r\n'.encode('utf-8')
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect((self.addr, self.port))
            connection.settimeout(16)
            connection.send(message)
            connection.recv(4096)
            #Get response from scanner
            try:
                barcode = connection.recv(4096)
                barcode = barcode.decode('utf-8')
            except socket.timeout:
                barcode = 'ERROR'
            connection.close()
            #Parse barcode and finish scanning if it is valid barcode found
            if 'X' in barcode:
                barcode = barcode.split(':')[0].replace('\r','')
                done = True
            #Finish scanning if timeout
            elif 'ERROR' in barcode:
                done = True
        return barcode