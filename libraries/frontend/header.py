#Version 23.08 Component to implement a row of indicators

import tkinter as tk

#Row of unlabeled indicators to be used as a header for a table or scrollable list
class Header(tk.Frame):
    def __init__(self, location, labels, color = '#F0F0F0'):
        #Create and configure widget
        parent = location[0]
        row    = location[1]
        column = location[2]
        tk.Frame.__init__(self, parent)
        self.grid(row = row, column = column, sticky = 'nsew')
        self.configure(
            background = '#F0F0F0',
            relief = 'solid'
        )
        #Create children widgets
        column = 0
        for i in labels:
            element = tk.Entry(self)
            element.insert(0,i)
            element.grid(row = 0, column = column, sticky = 'nsew')
            element.configure(
                background = '#FDFDFD',
                foreground = '#0F0F0F',
                highlightthickness = .5,
                highlightbackground = '#E0E0E0',
                highlightcolor = '#4BB5CD',
                relief = 'flat',
                justify = 'center',
                width = 12,
                state = 'disabled'
            )
            column = column + 1