#Imports

import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import datetime

#-----------Button Class---------------------------

#Standard Button
class Button(tk.Button):
    def __init__(self, location, label, handler):
        #Create and configure widget
        parent = location[0]
        row    = location[1]
        column = location[2]
        tk.Button.__init__(self, parent)
        self.grid(
            row = row, 
            column = column, 
            sticky = 'nsew', 
            padx=2, 
            pady=2
        )
        self.configure(
            background = '#99D5E3', 
            activebackground = '#4BB5CD', 
            foreground = '#0F0F0F',
            font = ('Segoe UI Bold',9),
            borderwidth = 0,
            relief = 'solid',
            padx = 5,
            pady = 3
        )
        self.label = label
        self.handler = handler
        self['text'] = label
        self['command'] = self.handle_event
    
    #Event Handler for when user presses button    
    def handle_event(self, *args):
        self.handler(self.label)
        
    #Change to normal button color and allow it to be pressed
    def enable(self):
        self['state'] = 'normal'
        self.configure(background = '#99D5E3')

    #Fade out button and prevent it from being pressed
    def disable(self):
        self['state'] = 'disabled'
        self.configure(background = '#C0C0C0')

#Button which replaces text with a picture        
class IconButton(Button):
    def __init__(self, location, label, handler, icon):
        #Create widget
        Button.__init__(self, location, label, handler)
        self.configure(background = '#F0F0F0')
        self.set_icon(icon, 15, 15)
        
    #Set picture file as icon
    def set_icon(self, icon, width, height): 
        file = f'C:\\Users\\{os.getlogin()}\\Documents\\repos\\SharedTools\\libraries\\frontend\\assets\\{icon}.png'
        icon = Image.open(file)
        icon = icon.resize((width, height), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(icon)
        self.configure(image = self.image)
        
    #Set color of label background
    def set_background_color(self, color):
        self.configure(background = color)
        
#IconButton with a label 
class LabeledIconButton(tk.Frame):
    def __init__(self, location, label, handler, icon):
        #Create widget
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
        self.label = label
        #Create children widgets
        self.widgets = {
            'Button' : IconButton((self,0,0), 'Add', handler, icon),
            'Label'  : tk.Label(self, text = label)
        }
        self.widgets['Label'].grid(
            row=0, 
            column=1, 
            sticky = tk.W
        )
        self.widgets['Label'].configure(
            background = '#F0F0F0',
            foreground = '#0F0F0F',
            font = ('Segoe UI Bold',9),
            highlightthickness = .5,
            highlightbackground = '#E0E0E0',
            highlightcolor = '#4BB5CD',
            relief = 'flat'
        )
        self.set_icon(icon, 20, 20)
               
    #Set color of label background
    def set_background_color(self, color):
        self.configure(background = color)
        self.widgets['Label'].configure(
            background = color,
            highlightbackground = color
        )
        self.widgets['Button'].configure(
            background = color,
            highlightbackground = color
        )

    #Set picture file as icon
    def set_icon(self, icon, width, height):
        self.widgets['Button'].set_icon(icon, width, height)
       
#Button preset configuration for HMI buttons        
class HMIButton(Button):
    def __init__(self, location, label, handler, data = 0):
        #Create widget
        Button.__init__(self, location, label, handler)
        self.configure(
            width = 11,
            height = 2,
            font = ('Arial Bold', 11)
        )
        self.data = data
        
    #Set color of label background
    def set_background_color(self, color):
        self.configure(background = color)
    
    #Event Handler for when user presses button    
    def handle_event(self, *args):
        self.handler(self.label, self.data)
    
    def set_active(self):
        self.configure(background = '#99D5E3',
            activebackground = '#4BB5CD',
            foreground = 'black')
        
    def set_pressed(self):
        self.configure(background = '#11667a',
            activebackground = '#4BB5CD',
            foreground = 'white')
        
    def set_green(self):
        self.configure(background = '#99e3be',
            activebackground = '#4bcd8d',
            foreground = 'black')
    
    def set_darkgreen(self):
        self.configure(background = '#107d3f',
        activebackground = '#107d3f',
        foreground = 'white')
        
        
#----------Containter------------------------------------------
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


#-------------------Scrollable----------------------------------------------
#Vertically scrollable list of elements
class Scrollable(tk.Frame):
    def __init__(self, location, dimensions):
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
        #Set up scrollable canvas
        width  = dimensions[0]
        height = dimensions[1]
        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient='vertical', command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar.configure(background = '#F0F0F0')
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(background='#F0F0F0')
        self.region = {}
        self.widgets = []
        self.clear()

    #Event Handler when scrolling is performed
    def on_scroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    #Clear all items in list of scrollable widgets, then recreate scrollable region
    def clear(self, *args):
        #Delete existing region
        if self.region:
            self.widgets.clear()
            self.region.destroy()
            self.canvas.delete("self.region")
            self.region = {}
        #Recreate region
        self.region = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window = self.region, anchor='nw', tags='self.region')
        self.region.bind("<Configure>", self.on_scroll)
        self.region.configure(background='#F0F0F0',padx = 5, pady = 5, highlightthickness = 0)
        self.canvas.yview_moveto('0.0')

#----------------------------Header----------------------------------------------------

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
            

            
#----------------------------Indicator-----------------------------------------------------
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
        
        
class Log(tk.Frame):
    def __init__(self, parent, row, column, width=200, height=200):
        #Create widget
        tk.Frame.__init__(self, parent)
        self.grid(row = row, column = column, sticky = 'nsew')
        self.configure(
            background = '#F0F0F0',
            borderwidth = 0,
            highlightthickness = .1,
            padx = 5, 
            pady=10, 
            relief = 'solid'
        )     
        self.message_limit = 10
        self.width = width
        #Generate children widgets
        self.widgets = {}
        self.widgets['Log']   = Scrollable((self, 0, 0), (width, height))
        self.widgets['Clear'] = Button((self,1,0), 'Clear', self.widgets['Log'].clear) 

    #Add statement to log
    def add(self, message_type, message):
        log = self.widgets['Log']
        length = len(log.widgets)
        #Add new statement
        log.widgets.append(Statement(log.region, message_type, message, length, self.width))
        #Remove oldest statements and shift remaining statements if message limit is given
        if length > self.message_limit:
            log.widgets.pop(0)
            for i in range(0, length):
                log.widgets[i].grid(row=i, column = 0)
        #Autoscroll to most recent log entry
        log.canvas.yview_moveto('1.0')

    #Set number of messages in log before oldest statements are removed 
    def set_message_limit(self, quantity):
        self.message_limit = quantity

class Statement(tk.Frame):
    def __init__(self, parent, message_type, message, row, width):
        #Create widget
        tk.Frame.__init__(self, parent)
        self.grid(row = row, column = 0, sticky = 'nsew')
        #Set color based on message type
        if message_type == 'INFO':
            foreground = '#2F813E'
            background = '#99E3A5'
        if message_type == 'ERROR':
            foreground = '#814C2F'
            background = '#E3B399'
        if message_type == 'ATTEMPT':
            foreground = '#0F0F0F'
            background = '#F0F0F0'
        #Generate text to output
        current_time = '{:%I:%M}'.format(datetime.datetime.now())
        filtered_message = message.replace('\r', '').replace('\n', '')
        #Generate log statement
        self.widgets = {
            'Time'    : tk.Label(self, text = current_time),
            'Message' : tk.Label(self, text = filtered_message)
        }
        self.configure(
            background = background,
            borderwidth = 0,
            relief = 'solid'
        )   
        self.widgets['Time'].grid(row = 0, column = 0, padx=1, sticky = tk.E)
        self.widgets['Message'].grid(row = 0, column = 1, padx = 4, sticky = tk.E)
        for i in self.widgets:
            self.widgets[i].configure(
                background = background, 
                foreground = foreground,
                borderwidth = 0,
                relief = 'solid', 
                anchor = 'w',
                font = ('Segoe UI',8)
            )
        self.widgets['Message'].configure(width = width)
        
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