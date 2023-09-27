#Version 23.08 Library to communicate with Epicor ERP System via REST

import requests
import base64

class Epicor:
    def __init__(self, config):
        #Extract all queries to Epicor Tables
        self.queries  = config['Queries']
        #Attempt login at startup
        if config['AuthType'] == 'Robot':
            self.token = config['Credentials']
        else:
            self.log_in(config['User'], config['Pass'])

    #Send query to Epicor Endpoint
    def send(self, service, parameters={}):
        query = self.queries[service]
        url = f'https://centralusdtapp30.epicorsaas.com/saas802/api/v1/BaqSvc{query}'
        if self.token:
            url = url.format(**parameters)
            headers = {'content-type': 'application/json', 'Authorization' : self.token}
            response = requests.get(url, headers = headers)
            response = response.json()['value']
        else:
            response = None
        return response

    #Provide login information to get authorized access to Epicor
    def log_in(self, username, password):
        success = False
        combo = '{username}:{password}'.format(username = username, password = password)
        auth  = base64.b64encode(combo.encode('ascii'))
        token = 'Basic {auth}'.format(auth = auth.decode('ascii'))
        headers = {'content-type': 'application/json', 'Authorization' : token}
        url = f'https://centralusdtapp30.epicorsaas.com/saas802/api/v1/BaqSvc{self.queries["Authentication"]}'
        response = requests.get(url, headers = headers, timeout = 3)
        if response.status_code == 200:
            self.token = token
            success = True
        else:
            self.token = None
        return success

    #Deactive authorized access to Epicor from current user
    def log_out(self):
        self.token = None