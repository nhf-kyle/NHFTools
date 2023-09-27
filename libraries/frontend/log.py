#Version 23.08 Composite component to implement a Log Widget

import datetime
import tkinter as tk

#Add shared libraries
import sys 
sys.path.insert(0, 'C:\\Documents\\repos\\SharedTools\\')
from libraries.frontend.scrollable import Scrollable
from libraries.frontend.button import Button

class Log(tk.Frame):
    def __init__(self, parent, row, column, width=200, height=200):
        #Create widget
        tk.Frame.__init__(self, parent)
        self.grid(row = row, column = column, sticky = 'nsew')
        self.configure(
            background = '#F0F0F0',
            borderwidth = 0,
            highlightthickness = .1,
            padx = 5, 
            pady=10, 
            relief = 'solid'
        )     
        self.message_limit = 10
        self.width = width
        #Generate children widgets
        self.widgets = {}
        self.widgets['Log']   = Scrollable((self, 0, 0), (width, height))
        self.widgets['Clear'] = Button((self,1,0), 'Clear', self.widgets['Log'].clear) 

    #Add statement to log
    def add(self, message_type, message):
        log = self.widgets['Log']
        length = len(log.widgets)
        #Add new statement
        log.widgets.append(Statement(log.region, message_type, message, length, self.width))
        #Remove oldest statements and shift remaining statements if message limit is given
        if length > self.message_limit:
            log.widgets.pop(0)
            for i in range(0, length):
                log.widgets[i].grid(row=i, column = 0)
        #Autoscroll to most recent log entry
        log.canvas.yview_moveto('1.0')

    #Set number of messages in log before oldest statements are removed 
    def set_message_limit(self, quantity):
        self.message_limit = quantity

class Statement(tk.Frame):
    def __init__(self, parent, message_type, message, row, width):
        #Create widget
        tk.Frame.__init__(self, parent)
        self.grid(row = row, column = 0, sticky = 'nsew')
        #Set color based on message type
        if message_type == 'INFO':
            foreground = '#2F813E'
            background = '#99E3A5'
        if message_type == 'ERROR':
            foreground = '#814C2F'
            background = '#E3B399'
        if message_type == 'ATTEMPT':
            foreground = '#0F0F0F'
            background = '#F0F0F0'
        #Generate text to output
        current_time = '{:%I:%M}'.format(datetime.datetime.now())
        filtered_message = message.replace('\r', '').replace('\n', '')
        #Generate log statement
        self.widgets = {
            'Time'    : tk.Label(self, text = current_time),
            'Message' : tk.Label(self, text = filtered_message)
        }
        self.configure(
            background = background,
            borderwidth = 0,
            relief = 'solid'
        )   
        self.widgets['Time'].grid(row = 0, column = 0, padx=1, sticky = tk.E)
        self.widgets['Message'].grid(row = 0, column = 1, padx = 4, sticky = tk.E)
        for i in self.widgets:
            self.widgets[i].configure(
                background = background, 
                foreground = foreground,
                borderwidth = 0,
                relief = 'solid', 
                anchor = 'w',
                font = ('Segoe UI',8)
            )
        self.widgets['Message'].configure(width = width)