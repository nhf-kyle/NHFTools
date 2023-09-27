#Version 23.01 Utility Class for performing REST operations to send/receive messages

import requests
import json
import numpy as np
from flask import Flask, jsonify

class RESTSender:
    def __init__(self, network):
        self.services = {}
        endpoints = config['Outputs']
        for item in endpoints:
            name = item['Name']
            addr = item['IP']
            port = f":{item['Port']}"
            url  = item['URL']
            self.services[name] = f'http://{addr}{port}{url}'

    #Send out a message to another API endpoint
    def send(self, service, message=''):
        url = self.services[service].format(message = message)
        response = requests.get(url)
        return response

class RESTReceiver:
    #Create a Flask instance
    def __init__(self, config):
        self.addr = config['IP']
        self.port = config['Port']
        self.app = Flask('__main__')
        self.endpoints = config['Inputs']
        
    #Connect Server Endpoint to Event Handler
    def add_endpoint(self, endpoint, handler):
        url = self.endpoints[endpoint]
        self.app.add_url_rule(url, endpoint, Event(self.app, handler))

    #Executes Flask instance
    def run(self):
        self.app.run(host = self.addr, port = self.port)
        
class Event:
    #Create Event Handler for URL
    def __init__(self, service, function):
        self.service = service
        self.function  = function

    #Execute event handler if URL is used
    def __call__(self, **kwargs):
        #Extract and transform arguments if they exist in REST message
        if kwargs:
            #Process and convert JSON and strings into dicts
            message = kwargs['message']
            if "'" in message:
                message = message.replace("'", '"')  
            request  = json.loads(message)
        else:
            request = kwargs
        answer   = self.function(request)
        response = self.service.make_response((jsonify(answer),200))
        return response
