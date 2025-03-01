import os, sys
import win32print
from PIL import Image
import PIL.ImageGrab as ImageGrab
from tkinter import filedialog
from tkinter import messagebox
from time import sleep
from tkinter import Toplevel



from print_ident_color import class_print
import tkinter as tk


import win32print
import win32ui
from PIL import Image, ImageWin

class print_class:
    def __init__(self, root):
        #root.overrideredirect(True) 
        self.root = root
    
        self.root.geometry("400x600+0+0") # width x height + X coordinate + Y coordinate
        self.root.resizable(width =False, height =False)
        
        root.attributes("-topmost", True)

        def get_info(self):

            loop = "fries"
            if loop is not None:
                # try: 
                #     filelocation = "C:/prctm_dog/canvas.png"
                #     img = ImageGrab.grab(bbox=(0, 0, 400, 600))
                #     img.save(filelocation)
                #     #canvas.update_idletasks()

                # except Exception as e:
                #     print(F"Error -> {e}")  
                canva = Toplevel(root) 
                self.pw = class_print(canva)
                self.root.after(100) 
                sleep(1)
                #self.pw.destroy_canvas()
                loop = None
                
                
            #    canvas.postscript(file=filename, colormode='color')
                
            #     img = Image.open("canvas.ps")  #abre el archivo .ps
            #     img.save("output_image.png", "PNG")
            #     with open(filename, 'rb') as flname:
            #         raw_data = flname.read() #read postcrip to raw data
            #         print("Raw data readed")


            #     return raw_data
            
            
    

        
                
                
                
        # def save_canvas():
            
            
if __name__ == "__main__":
    root = tk.Tk()
    application = print_class(root)
    root.mainloop()



        