#Version 23.08 Component for implementing standard toggle buttons

import tkinter as tk
from PIL import ImageTk, Image

#Add shared libraries
import sys 
sys.path.insert(0, 'C:\\Documents\\repos\\SharedTools\\')
from libraries.frontend.button import Button

#Standard Latch
class Latch(Button):
    def __init__(self, location, label, handler):
        #Create widget
        Button.__init__(self, location, label, handler)
        #Set initial state
        self.state = False
        self.refresh(self.state)
        
    #Overriden Event Handler for when user presses button (Acts as toggle)
    def handle_event(self, *args):
        self.state = not self.state 
        self.refresh(self.state)
        self.handler(self.label)
        
    #Refresh latch appearance based on state
    def refresh(self, state):
        if state:
            self.configure(
                background = '#4BB5CD',
                foreground = '#F0F0F0',
                relief = 'sunken'
            ) 
        else:
            self.config(relief = tk.RAISED)
            self.configure(
                background = '#99D5E3',
                foreground = '#0F0F0F',
                relief = 'raised'
            )
            
    #Get data encoded in widget
    def extract(self):
        content = {self.label: self.state}
        return content