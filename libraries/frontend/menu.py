#Version 23.08 Component for implementing standard menus

import tkinter as tk
from tkinter import ttk

#Standard Menu
class UnlabeledMenu(tk.Frame):
    def __init__(self, location, label, handler, options = None):
        #Create and configure widget
        parent = location[0]
        row    = location[1]
        column = location[2]
        tk.Frame.__init__(self, parent)
        self.grid(row = row, column = column, sticky = 'nsew')
        self.configure(
            background = '#F0F0F0',
            borderwidth = 0,
            relief = 'solid'
        )
        self.label = label
        self.handler = handler
        self.variable = tk.StringVar()
        #Create children widgets
        self.widgets = {}
        self.widgets['Value'] = ttk.Combobox(self, textvar = self.variable)
        self.widgets['Value'].grid(row = 0, column = 0, sticky = 'nsew')
        self.widgets['Value'].configure(
            background = '#FDFDFD', 
            foreground = '#0F0F0F',
            justify = 'center',
            width = 17
        )
        self.widgets['Value'].bind("<<ComboboxSelected>>", self.handle_event)
        self.variable.trace('w', self.bind)
        #Set initial list of options
        if options:
            self.set_options(options)

    #Event Handler for user selects an option from dropdown menu
    def handle_event(self, *args):
        content = self.extract()
        self.handler(content)

    #Set menu choice based on provided data
    def refresh(self, value):
        options = list(self.widgets['Value']['values'])
        choice  = str(value.replace("'",""))
        index   = options.index(choice)
        self.widgets['Value'].current(index)

    #Gets menu choice
    def extract(self):
        content = {self.label: self.widgets['Value'].get()}    
        return content

    #Reactivate menu widget and allow it to be modified
    def enable(self):
        self.widgets['Value'].configure(state = 'normal')        

    #Fade out menu widget and prevent it from being modified
    def disable(self):
        self.widgets['Value'].configure(state = 'disabled')    
        
    #Load set of options in dropdown menu
    def set_options(self, options):
        items = [i for i in options if (i != '') or (i != None)]
        self.widgets['Value']['values'] = items 
        self.refresh(items[0])
  
#Standard menu, combined with a text label          
class Menu(UnlabeledMenu):
    def __init__(self, location, label, handler, options = None):
        #Create widget
        UnlabeledMenu.__init__(self, location, label, handler, options)
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
            anchor = 'e'
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