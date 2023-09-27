#Version 23.08 Library to read/write data to Microsoft SQL Server database

import os
import sqlite3

#Class for communicating with SQLite  
class Database:
    def __init__(self, thread_flag = True):
        #Open existing SQLite database, or create a new one
        self.scripts_path = f'C:\\Users\\{os.getlogin()}\\Documents\\repos\\SharedTools\\libraries\\sql\\'
        self.script_cache = {}
        directory_list    = os.listdir(f'{os.getcwd()}\\backend\\')
        self.connection = sqlite3.connect(f'{os.getcwd()}\\backend\\local.db', check_same_thread = thread_flag)
        #If SQLite database was just created, initialize schema for it
        if 'local.db' not in directory_list:
            command = self.write('schema_createlocal')

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
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = []
        for row in cursor.fetchall():
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