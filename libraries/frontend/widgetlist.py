#Version 23.08 [UNSTABLE] Interface to implement list aggregation of homogeneous (single type) widgets
#Argument 'labels' are names specific to each widget in list 
#Argument 'handlers' are functions triggered during widget event (specific to each widget in list)
#Argument 'item_type' is a class for instantiating each item in list
#All listable widgets must have the following:
    #Required Arguments: self, parent, label, handler, row, column
    #Widgets cannot have any other required arguments
    #Widgets can have optional arguments. These can be set after instantiation of list
#TODO: Add methods to set consistent widths and heights for each widget

import tkinter as tk

#Row or column of widgets
class WidgetList(tk.Frame):
    def __init__(self, parent, item_type, labels, handlers, row, column, direction = 'vertical'):
        #Create widget
        tk.Frame.__init(self, parent)
        self.grid(row = row, column = column, sticky = 'nsew')
        self.configure(
            bg = 'white',
            borderwidth = 1,
            relief = 'solid'
        )
        self.iterable = iterable
        #Create children widgets
        self.widgets = {}
        index = 0
        for i in labels:
            if direction == 'vertical':
                element = self.item_type(self, labels[i], handlers[i], index, 0)
            if direction == 'horizontal':
                element = self.item_type(self, labels[i], handlers[i], 0, index)
            self.widgets[i] = element 
            index = index + 1
            
    #Set contents of children based on provided data
    def refresh(self, values):
        for i in values:
            self.widgets[i].refresh(values[i])
            
    #Get contents of children
    def extract(self):
        content = {}
        for i in self.widgets:
            content.update(self.widgets[i].extract())
        return content