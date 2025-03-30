#Archivo para ver las camaras del robot (deberian ser 5) y la rarita esa
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

class tracking_robot:
    
    def __init__(self, root):
        self.root = root
        
        root.overrideredirect(True)
        #root.resizable(width=False, height=False)
        style = ttk.Style()
        style.theme_use('clam')
        root.configure(bg='#1f1f1f')
        
        root.wm_attributes("-transparentcolor", "#1f1f1f" )
        
        self.root.attributes("-topmost", True)
        self.root.title("ROBOT TRACKING")
        self.root.geometry("800x750+25+15")
        
        #____________________________________________________FRAMES___________________________________________________#
    
        MainFrame = Frame(self.root, bd=5, width=800, height=750, relief=RIDGE, bg='#1f1f1f') #quitar al final
        MainFrame.grid()
        
        
        
        MainCamera = Frame(MainFrame, bd=5, width=790, height=440, relief=RIDGE, bg='#1f1f1f')
        MainCamera.grid(row=0, column=0, padx=5, pady=5)
        
        TheOtherCamera = Frame(MainCamera, bd=5, width=190, height=240, relief=RIDGE, bg='#1f1f1f')
        TheOtherCamera.grid(row=0, column=1, padx=5, pady=5)
        
        
        
        RemainsCameras = Frame(MainFrame, bd=5, width=790, height=340, relief=RIDGE, bg='#1f1f1f')
        RemainsCameras.grid(row=1, column=0)
        
        
        
        CameraSlot_1 = Frame(RemainsCameras, bd=5, width=160, height=140, relief=RIDGE, bg='#1f1f1f')
        CameraSlot_1.grid(row=0, column=0, padx=15, pady=25)
        
        CameraSlot_2 = Frame(RemainsCameras, bd=5, width=160, height=140, relief=RIDGE, bg='#1f1f1f')
        CameraSlot_2.grid(row=0, column=1, padx=15, pady=25)
        
        CameraSlot_3 = Frame(RemainsCameras, bd=5, width=160, height=140, relief=RIDGE, bg='#1f1f1f')
        CameraSlot_3.grid(row=0, column=2, padx=15, pady=25)
        
        CameraSlot_4 = Frame(RemainsCameras, bd=5, width=160, height=140, relief=RIDGE, bg='#1f1f1f')
        CameraSlot_4.grid(row=0, column=3, padx=15, pady=25)
        
        ButtonFrame = Frame(MainFrame, bd=5, width=790, height=90, relief=RIDGE, bg='#1f1f1f')
        ButtonFrame.grid(row=2, column=0)
        
        #____________________________________________________FUNCTIONS___________________________________________________#
        
        def hide_function():
            pass
        def unhide_function():
            pass
        
        def switch_camera_1():
            pass
        
if __name__ == "__main__":
    root = tk.Tk()
    app = tracking_robot(root)
    root.mainloop()