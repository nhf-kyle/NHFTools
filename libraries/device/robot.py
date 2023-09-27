#Version 23.08 Library to manipulate Fanuc R30iB Robots via REST, TCP, and FTP communication

import time
import socket
import requests

class Robot:
    def __init__(self, config, handler = None, register_flag = True):
        #Use parsed configuration settings to set up REST web server connection
        self.addr = config['Robot_IP']
        #Configure TCP Server if TCP IP is specified
        if config["TCP_IP"]:
            self.handler = handler
            self.receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.receiver.bind((config['TCP_IP'], config['TCP_Port']))
            self.receiver.listen()
        #Read all registers and flags into a cache
        if register_flag:
            self.bulk_read_registers()
            self.bulk_read_flags()

    #Set TCP Event Handler if not already set from constructor
    def set_tcp_handler(self, handler):
        self.handler = handler
        
    #Observe for TCP requests from robot, then respond with event handler
    def receive(self):
        while True:
            connection, addr = self.receiver.accept()
            data = connection.recv(1024)
            response = self.handler(data)
            connection.sendall(response)
        return data            
        
    #Read a single register or flag
    def read(self, tag_type, label):
        if tag_type == 'Register':
            index = self.registers[label]['index']
            endpoint = f'http://{self.addr}/KAREL/READ_REG?arguments={index}'
            response = requests.get(endpoint)
        if tag_type == 'Flag':
            index = self.flags[label]['index']
            endpoint = f'http://{self.addr}/KAREL/READ_FLG?arguments={index}'
            response = requests.get(endpoint)
        return response.json()

    #Write to single register or flag
    def write(self, tag_type, label, value):
        if tag_type == 'Register':
            index = self.registers[label]['index']
            pair  = f'{index},{value}'
            endpoint = f'http://{self.addr}/KAREL/SEND_REG?arguments={pair}'
            requests.get(endpoint)
        if tag_type == 'Flag':
            index = self.flags[label]['index']
            pair  = f'{index},{value}'
            endpoint = f'http://{self.addr}/KAREL/SEND_FLG?arguments={pair}'
            requests.get(endpoint)     

    #Get regular files from Robot (for large persistent files)
    def get_file(self, filename):
        endpoint = f'http://{self.addr}/FR/{filename}.dat'
        response = requests.get(endpoint)
        return response.content

    #Get regular files from Robot (for large persistent files)
    def get_pipe_file(self, filename):
        endpoint = f'http://{self.addr}/PIP/{filename}.dat'
        response = requests.get(endpoint)
        result   = response.content[1:].decode()
        result   = result.split('\n')
        result.remove('')
        return result

    #Append each line of a message to a specified pipe file (Lines have a limit of 254 characters)
    def send_pipe_file(self, filename, message):
        #Clear pipe file of previous contents
        arguments = f'{filename}|CLEAR'
        endpoint = f'http://{self.addr}/KAREL/SEND_PIP?arguments={arguments}'
        requests.get(endpoint)
        #If messages argument is a string, convert it to an array of strings 
        if type(message) == str:
            message = [message]
        #Write message to pipe file, one line at a time
        for line in message:
            arguments = f"{filename}|{line}"
            endpoint = f'http://{self.addr}/KAREL/SEND_PIP?arguments={arguments}'
            requests.get(endpoint)

    #Write to multiple registers at once
    #DEPRECATE THIS. IF WE NEED TO BULK WRITE, use PIPE FILES
    def bulk_write(self, tags):
        #Parse tag dictionary into consolidated Fanuc string
        packets = []
        message = ''
        last_item = list(tags)[-1]
        for item in tags:
            index = self.registers[item]['index']
            value = round(tags[item], 4)
            message = ';'.join([message, f'{index},{value}'])
            #Split message into packets to avoid issues with 254 char limit of Karel Strings
            if (len(message) > 240) or (item == last_item) :
                packets.append(message)
                message = ''
        #Send each packet to robot 
        for message in packets:
            endpoint = f'http://{self.addr}/KAREL/SEND_REG?arguments={message}'
            requests.get(endpoint)

    #Read all robot registers
    def bulk_read_registers(self):
        #Retrieve registers file from Fanuc Web Server
        endpoint = f'http://{self.addr}/MD/NUMREG.VA'
        response = requests.get(endpoint)
        #Parse and segment file into individual register data
        trimmed = str(response.content).split("Reg\\r\\n  [")[1]
        trimmed = trimmed.split(" \\r\\n\\r\\n[*NUMREG*]")[0]
        segmented = trimmed.split("\\' \\r\\n  [")
        registers = {}
        for item in segmented:
            first_partition  = item.split('] = ')
            second_partition = first_partition[1].split("  \\'")
            index     = int(first_partition[0])
            value     = second_partition[0]
            label     = second_partition[1]
            registers[label] = {'index' : index, 'value': value}       
        self.registers = registers
        
    #Read all robot flags
    def bulk_read_flags(self):
        #Retrieve registers file from Fanuc Web Server
        endpoint = f'http://{self.addr}/MD/IOSTATE.DG'
        response = requests.get(endpoint)
        #Parse and segment file into individual register data
        trimmed = str(response.content).split('RO[   8] OFF  \\n')[1]
        trimmed = trimmed.split('\\n</PRE>\\n</BODY>\\n</HTML>\\n\\n')[0]
        #trimmed = trimmed.replace(' ','')
        trimmed = trimmed.replace('\\n','')
        segmented = trimmed.split('FLG[')[1:]
        flags = {}
        for item in segmented:
            first_partition = item.split(']')
            index = first_partition[0]
            second_partition = first_partition[1]
            if 'OFF' in second_partition.replace(' ','')[0:3]:
                value = False
                label = second_partition.split('OFF')[1].strip()
            if 'ON' in second_partition.replace(' ','')[0:3]:
                value = True
                label = second_partition.split('ON')[1].strip()
            if label:
                flags[label] = {'index' : index, 'value': value}
        self.flags = flags