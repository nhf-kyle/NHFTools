#Version 23.08 Component for implementing standard text entry fields
#TODO: Should 'validate' function be part of GUI or controller?

import tkinter as tk

#Standard Entry Field
class UnlabeledField(tk.Frame):
    def __init__(self, location, label, handler, validate_type = None):
        #Create and configure widget
        parent = location[0]
        row    = location[1]
        column = location[2]
        tk.Frame.__init__(self, parent)
        self.grid(row = row, column = column, sticky = 'nsew')
        self.configure(background = '#F0F0F0', relief = 'solid')
        self.label = label
        self.handler = handler
        self.validate_type = validate_type
        #Create children widgets
        self.widgets = {}
        self.widgets['Value'] = tk.Entry(self)
        self.widgets['Value'].grid(row = 0, column = 0, sticky = tk.W)
        self.widgets['Value'].configure(
            background = '#FDFDFD',
            foreground = '#0F0F0F',
            highlightthickness = .5,
            highlightbackground = '#E0E0E0',
            highlightcolor = '#4BB5CD',
            relief = 'flat',
            justify = 'center',
            width = 12
        )
        self.widgets['Value'].bind("<KeyRelease>", self.handle_input)
        self.widgets['Value'].bind("<Return>", self.handle_enter)
        self.enter_handler = None
        
    #Event Handler for when user writes in field
    def handle_input(self, *args):
        if self.validate():
            content = self.extract()
            self.handler(content)
    
    #Event Handler for when user presses enter button
    def handle_enter(self, *args):
        if self.enter_handler:
            self.enter_handler()

    #Bind event handler for Enter Key Press
    def set_enter_handler(self, handler):
        self.enter_handler = handler

    #Set field contents based on provided data
    def refresh(self, value):
        self.widgets['Value'].delete(0,tk.END)
        self.widgets['Value'].insert(0,value)
        self.widgets['Value'].config({"background": "White"})
        self.validate()

    #Gets field contents
    def extract(self):
        content = {self.label: self.widgets['Value'].get()}    
        return content

    #Reactivate entry widget and allow it to be modified
    def enable(self):
        self.widgets['Value'].delete(0, tk.END)
        self.widgets['Value'].configure(
            state = 'normal',
            background = '#FDFDFD'
        )
        self.validate()      

    #Fade out entry widget and prevent it from being modified
    def disable(self, keep_value = False):
        if not keep_value:
            self.widgets['Value'].delete(0, tk.END)
        self.widgets['Value'].configure(
            state = 'disabled',
            background = '#C0C0C0'
        )        

    #Set up field for blocking out passwords
    def hide_text(self):
        self.widgets['Value'].configure(show = '*')

    #Set validate type (if not already set during instantiation)
    def set_validate_type(self, value):
        self.validate_type = value

    #Set width of field
    def set_field_width(self, width):
        self.widgets['Value'].configure(width = width)
        
    #Indicate if value inside field is valid based on type
    def validate(self):
        success = True
        value = self.widgets['Value'].get()
        #Validate for integers
        if self.validate_type == 'int':
            success = False if not value.isnumeric() else True
        #Validate for floats
        if self.validate_type == 'float':
            try:
                isinstance(float(value), float)
            except ValueError:
                success = False
        #Validate for UA numbers
        if self.validate_type == 'UA':
            success = False
            if 'UA' in value:
                project, serial = value.split('UA')
                if project.isnumeric() and serial.isnumeric():
                    if (len(project) == 4) and (len(serial) == 5):
                        success = True
        #Highlight field as red if value is invalid
        color = "#F0C8C8" if not success else "White"
        self.widgets['Value'].config({"background": color})
        return success
  
#Standard field, combined with a text label        
class Field(UnlabeledField):
    def __init__(self, location, label, handler, validate_type = None):
        #Create widget
        UnlabeledField.__init__(self, location, label, handler, validate_type)
        #Add label component, then rearrange appearance
        self.widgets['Value'].grid(row = 0, column = 1, sticky = tk.W)
        self.widgets['Value'].configure(
            borderwidth = 0,
            highlightbackground = '#101010',
            width = 20
        )
        self.widgets['Label'] = tk.Label(self, text = f'{label}: ')
        self.widgets['Label'].grid(row = 0, column = 0, sticky = tk.E)
        self.widgets['Label'].configure(
            background = '#F0F0F0',
            foreground = '#0F0F0F',
            font = ('Segoe UI Bold',9),
            borderwidth = 0, 
            anchor = 'e',
            relief = 'solid'
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