#Version 23.08 Interface to implement scrolling for a container

import tkinter as tk

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
