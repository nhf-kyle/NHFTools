#Version 23.08 Component to implement spacing between components

import tkinter as tk

#Widget to add fixed space between other widgets
class Spacer(tk.Label):
    def __init__(self, location, width = 0, height = 0, rowspan = 1, columnspan = 2):
        parent = location[0]
        row    = location[1]
        column = location[2]
        #Create widget
        tk.Label.__init__(self, parent, text = '')
        self.grid(
            row = row, 
            column = column, 
            rowspan = rowspan, 
            columnspan = columnspan, 
            sticky = 'nsew'
        )
        self.configure(
            background = '#F0F0F0',
            padx = width,
            pady = height
        )
        
    #Set color of label background
    def set_background_color(self, color):
        self.configure(background = color)