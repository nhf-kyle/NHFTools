#Version 23.08 Component to implement a standard title

import tkinter as tk

#Widget that contains only title text
class Title(tk.Label):
    def __init__(self, location, label, columnspan = 2):
        parent = location[0]
        row    = location[1]
        column = location[2]
        #Create widget
        tk.Label.__init__(self, parent, text = label)
        self.grid(
            row = row, 
            column = column, 
            columnspan = columnspan, 
            sticky = 'nsew'
        )
        self.configure(
            background = '#F0F0F0', 
            foreground = '#0F0F0F',
            font = ('Segoe UI Bold', 11)
        )
        
    #Set text to display
    def set_text(self, value):
        self['text'] = value
        
    #Set color of label background
    def set_background_color(self, color):
        self.configure(background = color)