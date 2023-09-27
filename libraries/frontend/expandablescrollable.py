#Version 23.08 [UNSTABLE] Scrollable widget with an add button to increment number of elements

import tkinter as tk

#Add shared libraries
import os
import sys 
sys.path.insert(0, f'C:\\Users\\{os.getlogin()}\\Documents\\repos\\SharedTools\\')
from libraries.frontend.scrollable import Scrollable
from libraries.frontend.header import Header
from libraries.frontend.button import Button, IconButton

#NOTES ON USAGE:
#'ExpandableScrollable' contains the following:
#1) List of single-type widgets (each with the same handler and label, only different by index)

#1) Classes which inherit 'ExpandableScrollable' must pass 'Add' and 'Delete' handlers 
    #- 'Add' handler is invoked whenever the 'Add' button is pressed
    #- 'Delete' handler is invoked whenever the 'Delete' button is pressed by individual list entries
#2) List Type should be a class which inherits the 'ListItem' class defined below

class ExpandableList(Scrollable):
    def __init__(self, parent, controller, item_type, handlers, row, column, width, height, header = None):
        #Create Widget
        Scrollable.__init__(self, parent, row, column, width, height)
        self.controller = controller
        self.header = header
        self.item_type = item_type
        self.handlers = {
            'Add'   : handlers['Add']
            'Delete': handlers['Delete']
            'Modify': handlers['Modify']
        }handler
        
    def refresh(self, data):
        self.clear()
        self.widgets['Header'] = Header(self.region, self.header, 0, 0, color = '#F3CCAA')
        row = 1
        for content in data:
            element = self.item_type(self.region, self.controller, content, row, 0)
            element.widgets['Delete'] = IconButton(element, f'Delete{row}', self.delete, 'remove', 0, len(element.widgets))
            self.widgets[row] = element
            row = row+1
        self.widgets['Add'] = IconButton(self.region, 'Add', self.add, 'add', len(self.widgets), 0)
 
    def delete(self, label):
        index = int(label.replace('Delete',''))
        content = self.widgets[index].extract()
        self.handlers['Delete'](content)
        self.controller.delete_pane(content)
        
    def add(self):
        self.handlers['Add']()

    #Refresh list based on given data
    def refresh(self, data):
        self.clear()
        for content in data:
            element = self.list_type(self.region, self.controller, self.handlers, row, 0)
            self.items.append(element)
            index = len(self.items)
            self.items[row].refresh(content, index)