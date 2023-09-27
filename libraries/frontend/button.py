#Version 23.08 Component for implementing standard and icon buttons

import os
import tkinter as tk
from PIL import ImageTk, Image

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