import os, sys
import win32print
from PIL import Image
import PIL.ImageGrab as ImageGrab
from tkinter import filedialog
from tkinter import Label
from time import sleep
from tkinter import Toplevel

from print_ident_color import class_print
import tkinter as tk
from tkinter import Tk

import win32print
import win32ui
from PIL import Image, ImageWin

class print_class:
    def __init__(self, root):
        root.overrideredirect(True) 
        self.root = root
        
        self.root.geometry("250x75") # width x height + X coordinate + Y coordinate
        self.root.resizable(width =False, height =False)
        root.attributes("-topmost", True)
        
        root.withdraw()
        root.update_idletasks()  # Update "requested size" from geometry manager <--- Hack
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.geometry("+%d+%d" % (x, y))
        #_____________________________________________FUNCTIONS_____________________________________________#
        
        
        
        def save_as_png(self):
                    root.deiconify()
                    Label(root, text="PRINTING DATA...").pack()
                    self.file = "C:/prctm_dog/canvas.png"
                    ImageGrab.grab().crop((346,60,390,106)).save(self.file)
        
        def edit_canvas(self):
            
            #obtener las variables
            
            window_canvas = Toplevel(self.root)
            self.canvitas = class_print(window_canvas)
            self.root.after(3000)
            # self.root.after(100, save_as_png(self))
            
            try:
                self.canvitas.setup_gamer()
                #editar esto para poner las variables
                self.canvitas.info("FBI2", 123456782, "strange2", "nm & ln 2")
            except Exception as e:
                print(f"No se que le pasa :(\n{e}")

            self.root.after(3000)
            save_as_png(self)
      
        edit_canvas(self)

            
if __name__ == "__main__":
    root = tk.Tk()
    application = print_class(root)
    root.mainloop()


