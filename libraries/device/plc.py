#Version 23.08 Library to communicate with Allen Bradley CompactLogix and ControlLogix PLCs (to read and write tags)
 
import pylogix

class PLC:
    def __init__(self, settings):
        #Initialize Attributes
        self.connection = {}
        self.ip = settings['IP']
        self.tags = []
        #Connect to PLC
        self.connect()
        self.status = self.check_connection()
        self.disconnect()

    #Read specified tag's value
    def read(self, tag):
        self.connect()
        value = self.connection.Read(tag)
        self.disconnect()
        return value.Value
        
    #Write to specified tag
    def write(self, tag, value):
        self.connect()
        self.connection.Write(tag, value)
        self.disconnect()

    #Pulse a tag for specified amount of time
    def pulse(self, tag, pulse_length = 2.0, polarity = 'Normal'):
        self.connect()
        if polarity == 'Normal':
            high = 1
            low  = 0
        elif polarity == 'inverse':
            high = 0
            low  = 1
        self.connection.Write(tag, high)
        time.sleep(pulse_length)
        self.connection.Write(tag, low)

    #Check if PLC is connected 
    def check_connection(self):
        self.connection.SocketTimeout = 0.5
        response = self.connection.GetDeviceProperties()
        self.connection.SocketTimeout = 5.0
        if response.Status == 'Success':
            return True
        else:
            return False
            
    #Connect to PLC at specified address
    def connect(self):
        self.connection = pylogix.PLC()
        self.connection.IPAddress = self.ip
        
    #Close PLC connection when finished
    def disconnect(self):
        self.connection.Close()

    #Look up all tags in PLC
    def discover_tags(self):
        self.connect()
        tags = self.connection.GetTagList()
        for t in tags.Value:
            self.tags.append(t.TagName)