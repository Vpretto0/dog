import camera_1
import camera_2
import camera_3
import camera_4
#import cv2, socket y todo eso

#plan: obtener todas las camaras, hacer que se puedan cambiar de poscicion y de tamano, y que se puedan ver todas al mismo tiempo.
#en el futuro, pordas trakear objetos y seguirlos desde la camara que este seleccionada

import tkinter as tk



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
        self.root.geometry("800x750+25+25")
        
        #____________________________________________________FRAMES___________________________________________________#
    
        MainFrame = Frame(self.root, bd=5, width=800, height=750, relief=RIDGE, bg='#1f1f1f') #quitar al final
        MainFrame.grid()
        