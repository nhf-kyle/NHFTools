#Version 23.08 Interface for implementing a generic tkinter widget based on tk.Frame

import tkinter as tk

class Container(tk.Frame):
    def __init__(self, location, controller = None):
        #Create and configure widget
        parent = location[0]
        row    = location[1]
        column = location[2]
        tk.Frame.__init__(self, parent)
        self.grid(
            row = row, 
            column = column, 
            sticky = 'nsew'
        )
        self.configure(
            background = '#F0F0F0',
            relief = 'solid'
        )
        #Set up attributes
        self.controller = controller
        self.widgets = {}

    #Set content for all refreshable child widgets based on provided data
    def refresh(self, data):
        for i in self.widgets:
            content = data[i] if i in data else data
            element = self.widgets[i]
            if hasattr(element, 'refresh'):
                element.refresh(content)
                
    #Set dimensions of children widgets based on widest child
    def resize(self):
        resizables = []
        for i in self.widgets:
            element = self.widgets[i]
            if hasattr(element, 'get_width') and hasattr(element, 'set_width'):
                resizables.append(element)
        widths = [i.get_width() for i in resizables]
        if widths:
            max_width = max(widths)
            for i in resizables:
                i.set_width(max_width)
                
    #Set color for widget
    def set_background_color(self, color):
        self.configure(background = color)
        for i in self.widgets:
            element = self.widgets[i]
            if hasattr(element, 'set_background_color'):
                element.set_background_color(color)