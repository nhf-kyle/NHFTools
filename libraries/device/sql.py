#Version 23.08 Library to read/write data to Microsoft SQL Server database

import os
import pyodbc
 
class Database:
    def __init__(self, config):
        #Attributes
        self.scripts_path = f'C:\\Users\\{os.getlogin()}\\Documents\\repos\\SharedTools\\libraries\\sql\\'
        self.script_cache = {}
        #Open connection to Microsoft SQL Server
        connectionstring = config['Credentials'].replace('\n','')
        database = pyodbc.connect(connectionstring, timeout = 2)
        self.connection = database.cursor()

    #Execute read operation via a SQL script file 
    def read(self, script, **params):
        query  = self.retrieve_script(script)
        query  = query.format(**params)
        result = self.read_raw(query)
        return result

    #Execute write operation via a SQL script file       
    def write(self, script, **params):
        command  = self.retrieve_script(script)
        command  = command.format(**params)
        self.write_raw(command)

    #Execute read operations via a raw string containing a SQL query
    def read_raw(self, query):
        self.connection.execute(query)
        results = []
        for row in self.connection.fetchall():
            results.append(row)
        if len(results) > 0 and len(results[0]) == 1:
            results = [item[0] for item in results]
        return results
        
    #Execute write operation via a raw string containing a SQL command
    def write_raw(self,command):
        statements = [item for item in command.split(';') if item != '']
        for command in statements:
            self.connection.execute(command)
            self.connection.commit()

    #Get query/command from cache, otherwise open/parse/cache it
    def retrieve_script(self, label):
        if label not in self.script_cache:
            with open(f"{self.scripts_path}{label}.sql", 'r') as file:
                value = file.read().replace('    ',' ')
                value = value.replace('\n','').replace('  ',' ')
                self.script_cache[label] = value
        script = self.script_cache[label]
        return script
            
    #Empty all contents inside database
    def clear_contents(self):
        #Recreate database schema
        script  = self.retrieve_script('schema_createserver')
        self.write(script)