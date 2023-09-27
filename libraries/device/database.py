#Version 23.08 Library to manipulate content from 'FrameData' database (or SQLite session with FrameData schema)

#Add libraries from shared repository
import os
import sys
sys.path.insert(0, f'C:\\Users\\{os.getlogin()}\\Documents\\repos\\SharedTools\\')
from libraries.device.sql import Database as SQL
from libraries.device.sqlite import Database as SQLite

class Database:
    def __init__(self, connectionstring, session_flag = False):
        #Initialize server database connection
        self.data = {}
        self.data['Server'] = SQL(connectionstring)
        #Initialize local database for usage as a session
        if session_flag:
            self.data['Local'] = SQLite()
  
    #-----------------------------------------------------------------------------------------------
    #Migration Functionality
    #-----------------------------------------------------------------------------------------------

    #Check if unit exists in database
    def check_exists(self, unit, location = 'Server'):
        result = self.data[location].read_raw(f"SELECT 1 FROM unit WHERE ua_number = '{unit}'")
        return result

    #Pull relational data from specified database
    def download(self, unit, source = 'Server'):
        content = {
            'Unit'         : self.read_unit(unit, source),
            'Panes'        : self.read_panes(unit, source),
            'Edges'        : self.read_edges(unit, source),
            'Obstructions' : self.read_obstructions(unit, source)
        }
        return content
        
    #Push relational data to specified database
    def upload(self, content, destination = 'Server'):
        unit = content['Unit']
        ua = unit['Unit']
        #Insert or update for tables
        self.upsert_unit(unit, destination)
        for pane in content['Panes']:
            self.upsert_pane(pane, destination)
        for edge in content['Edges']:
            self.upsert_edge(edge, destination)
        for obstruction in content['Obstructions']:
            self.upsert_obstruction(obstruction, destination)
        #Delete obstructions that don't exist on GUI
        nonremovable = []
        data = self.read_obstructions(ua, destination)
        for i in data:
            for j in content['Obstructions']:
                pane_match = (i['Pane'] == j['Pane'])
                edge_match = (i['Edge'] == j['Edge'])
                obstruction_match = (i['Obstruction'] == j['Obstruction'])
                if pane_match and edge_match and obstruction_match:
                    nonremovable.append(i)
        removable = [i for i in data if i not in nonremovable]
        for item in removable:
            self.delete_obstruction(item, destination)
        #Delete edges that don't exist on GUI
        nonremovable = []
        data = self.read_edges(ua, destination)
        for i in data:
            for j in content['Edges']:
                pane_match = (i['Pane'] == j['Pane'])
                edge_match = (i['Edge'] == j['Edge'])
                if pane_match and edge_match:
                    nonremovable.append(i)
        removable = [i for i in data if i not in nonremovable]
        for item in removable:
            self.delete_edge(item, destination)
        #Delete panes that don't exist on GUI
        nonremovable = []
        data = self.read_panes(ua, destination)
        for i in data:
            for j in content['Panes']:
                pane_match = (i['Pane'] == j['Pane'])
                if pane_match:
                    nonremovable.append(i)
        removable = [i for i in data if i not in nonremovable]
        for item in removable:
            self.delete_pane(item, destination)

    #-----------------------------------------------------------------------------------------------
    #Unit Table
    #-----------------------------------------------------------------------------------------------

    #Read unit table information from database for a specified unit
    def read_unit(self, unit, location = 'Server'):
        data = {}
        parameters = {'unit': unit}
        response = self.data[location].read('unit_read', **parameters)
        if response:
            data['Unit']  = unit
            data['Width'] = round(response[0][1], 3)
        return data

    #Creates or update a unit with specified content
    def upsert_unit(self, content, location = 'Server'):
        parameters = {
            'unit' : content['Unit'],
            'width': content['Width']
        }
        self.data[location].write('unit_upsert', **parameters)

    #Delete a unit and its associated panes, edges, and obstructions
    def delete_unit(self, unit, location = 'Server'):
        parameters = {'unit': unit}
        self.data[location].write('unit_delete', **parameters)

    #-----------------------------------------------------------------------------------------------
    #Pane Table
    #-----------------------------------------------------------------------------------------------

    #Read pane table information from database for a specified unit
    def read_panes(self, unit, location = 'Server'):
        data = []
        parameters = {'unit': unit}
        response = self.data[location].read('pane_read', **parameters)
        for item in response:
            data.append({
                'Unit'        : unit,
                'Pane'        : int(item[1]),
                'Plunge Depth': round(item[2], 3)
            })
        return data
    
    #Creates or update a pane with specified content
    def upsert_pane(self, content, location = 'Server'):
        parameters = {
            'unit'        : content['Unit'],
            'pane_number' : content['Pane'],
            'plunge_depth': content['Plunge Depth']
        }
        self.data[location].write('pane_upsert', **parameters)

    #Delete a pane and its associated edges and obstructions
    def delete_pane(self, content, location = 'Server'):
        parameters = {
            'unit'       : content['Unit'],
            'pane_number': content['Pane']
        }
        self.data[location].write('pane_delete', **parameters)



    #-----------------------------------------------------------------------------------------------
    #Edge Table
    #-----------------------------------------------------------------------------------------------

    #Read edge table information from database for a specified unit
    def read_edges(self, unit, location = 'Server'):
        data = []
        parameters = {'unit': unit}
        response = self.data[location].read('edge_read', **parameters)
        for item in response:
            data.append({
                'Unit'      : unit,
                'Pane'      : int(item[0]),
                'Edge'      : int(item[1]),
                'Edge Type' : int(item[4]),
                'Fill Area' : round(item[5], 3),
                'X Start'   : round(item[6], 3),
                'Y Start'   : round(item[7], 3),
                'Z Start'   : round(item[8], 3),
                'X Stop'    : round(item[9], 3),
                'Y Stop'    : round(item[10], 3),
                'Z Stop'    : round(item[11], 3)
            })
        return data

    #Creates or update an edge with specified content
    def upsert_edge(self, content, location = 'Server'):
        parameters = {
            'unit'        : content['Unit'],
            'pane_number' : content['Pane'],
            'edge_number' : content['Edge'],
            'edge_type'   : content['Edge Type'],
            'fill_area'   : content['Fill Area'],
            'x0'          : content['X Start'],
            'y0'          : content['Y Start'],
            'z0'          : content['Z Start'],
            'x1'          : content['X Stop'],
            'y1'          : content['Y Stop'],
            'z1'          : content['Z Stop']
        }
        self.data[location].write('edge_upsert', **parameters)  
 
    #Delete edge and its associated obstructions
    def delete_edge(self, content, location = 'Server'):
        parameters = {
            'unit'       : content['Unit'],
            'pane_number': content['Pane'],
            'edge_number': content['Edge']
        }
        self.data[location].write('edge_delete', **parameters)        

    #-----------------------------------------------------------------------------------------------
    #Obstruction Table
    #-----------------------------------------------------------------------------------------------

    #Read obstruction table information from database for a specified unit
    def read_obstructions(self, unit, location = 'Server'):
        data = []
        parameters = {'unit': unit}
        response = self.data[location].read('obstruction_read', **parameters)
        for item in response:
            data.append({
                'Unit'        : unit,
                'Pane'        : int(item[0]),
                'Edge'        : int(item[1]),
                'Obstruction' : int(item[2]),
                'Search Type' : int(item[3]),
                'Track Type'  : int(item[4]),
                'Offset'      : round(item[5], 3),
                'Width'       : round(item[6], 3)
            })
        return data

    #Creates or update an obstruction with specified content
    def upsert_obstruction(self, content, location = 'Server'):
        parameters = {
            'unit'              : content['Unit'],
            'pane_number'       : content['Pane'],
            'edge_number'       : content['Edge'],
            'obstruction_number': content['Obstruction'],
            'search_type'       : content['Search Type'],
            'track_type'        : content['Track Type'],
            'offset'            : content['Offset'],
            'width'             : content['Width']
        }
        self.data[location].write('obstruction_upsert', **parameters)  
 
    #Delete obstruction 
    def delete_obstruction(self, content, location = 'Server'):
        parameters = {
            'unit'       : content['Unit'],
            'pane_number': content['Pane'],
            'edge_number': content['Edge'],
            'obstruction_number': content['Obstruction']
        }
        self.data[location].write('obstruction_delete', **parameters)     