#Version 23.08 Component for displaying a static image

import tkinter as tk 
from PIL import ImageTk, Image

#Widget for displaying image
class ImageDisplay(tk.Label):
    def __init__(self, location, dimensions, imagepath):
        parent = location[0]
        row    = location[1]
        column = location[2]
        tk.Label.__init__(self, parent)
        self.grid(
            row = row, 
            column = column, 
            sticky = 'nsew', 
            padx = 3
        )
        #Load and configure image
        file  = Image.open(imagepath)
        file  = file.resize(dimensions, Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(file)
        self.configure(
            bg = 'white', 
            borderwidth = 0
            image = self.image
        )
