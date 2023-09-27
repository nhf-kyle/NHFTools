#Version 23.08 Component for implementing standard text indicators

import tkinter as tk

#Standard indicator 
class UnlabeledIndicator(tk.Frame):
    def __init__(self, parent, row, column):
        #Create widget
        tk.Frame.__init__(self, parent)
        self.grid(row = row, column = column, sticky = 'nsew')
        self.configure(
            background = '#F0F0F0',
            borderwidth = 0,
            relief = 'solid'
        )
        #Create children widgets
        self.widgets = {}
        self.widgets['Value'] = tk.Label(self)
        self.widgets['Value'].grid(row = 0, column = 0, sticky = tk.W)
        self.widgets['Value'].configure(
            background = '#FDFDFD', 
            foreground = '#0F0F0F',
            borderwidth = .5,
            relief = 'solid', 
            justify = 'center',
            width = 17
        )
        
    #Change text value
    def refresh(self, value):
        self.widgets['Value']['text'] = value
        
    #Change color of text
    def set_foreground(self, color):
        self.widgets['Value'].configure(foreground=color)
        
    #Change color of background
    def set_background(self, color):
        self.widgets['Value'].configure(background=color)
        
    #Set indicator to commonly used indicator values
    def set_status(self, status, value = None):
        if not value:
            value = status
        if status == 'Pass':
            self.refresh(value)
            self.set_foreground('#2F813E')
            self.set_background('#99E3A5')
        if status == 'Fail':
            self.refresh(value)
            self.set_foreground('#814C2F')
            self.set_background('#E3B399')
        if status == 'Warn':
            self.refresh(value)
            self.set_foreground('#81742F')
            self.set_background('#E3CD53')             

#Standard indicator, combined with a text label
class Indicator(UnlabeledIndicator):
    def __init__(self, parent, label, row, column):
        #Create widget
        UnlabeledIndicator.__init__(self, parent, row, column)
        #Add label component, then rearrange appearance
        self.widgets['Value'].grid(row = 0, column = 1, sticky = tk.W)
        self.widgets['Label'] = tk.Label(self, text = f'{label}: ')
        self.widgets['Label'].grid(row = 0, column = 0, sticky = tk.E)
        self.widgets['Label'].configure(
            background = '#F0F0F0',
            foreground = '#0F0F0F',
            font = ('Segoe UI Bold',9),
            borderwidth = 0, 
            relief = 'solid', 
            anchor = 'e',
        )
        
    #Get width of label
    def get_width(self):
        width = len(self.widgets['Label']['text'])
        return width

    #Set width of label
    def set_width(self, width):
        self.widgets['Label'].configure(width = width)
        
    #Set color of label background
    def set_background_color(self, color):
        self.widgets['Label'].configure(background = color)
        self.configure(background = color)