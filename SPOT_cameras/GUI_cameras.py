import camera_1
import camera_2
import camera_3
import camera_4
import camera_5
#import cv2, socket y todo eso

#plan: obtener todas las camaras, hacer que se puedan cambiar de poscicion y de tamano, y que se puedan ver todas al mismo tiempo.
#en el futuro, pordas trakear objetos y seguirlos desde la camara que este seleccionada

import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk

positions = { 1 : 1, 2 : 2, 3 : 3, 4 : 4, 5 : 5} #pos : cam      //DICCIONARIO
class Camera_guy:
    
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
        
        self.main_pos = 1   #si no funciona poner abajo
        self.init_cameras()
        
        #____________________________________________________FRAMES___________________________________________________#
    
        self.MainFrame = Frame(self.root, bd=5, width=800, height=750, relief=RIDGE, bg='#1f1f1f') 
        self.MainFrame.grid()
        
        self.ImageOnMainCamera = Frame(self.MainFrame, bd=5, width=800, height=750, relief=RIDGE, bg='#1f1f1f')
        self.ImageOnMainCamera.grid(row=0, column=0)
        
        self.MainCameraPos = Frame(self.MainFrame, bd=5, width=800, height=750, relief=RIDGE, bg='#1f1f1f')
        self.MainCameraPos.grid(row=0, column=1)
        
        self.SecondaryCamerasCont = Frame(self.MainFrame, bd=5, width=800, height=750, relief=RIDGE, bg='#1f1f1f')
        self.SecondaryCamerasCont.grid(row=0, column=2)
        
        self.SecondCameraPos = Frame(self.SecondaryCamerasCont, bd=5, width=800, height=750, relief=RIDGE, bg='#1f1f1f')
        self.SecondCameraPos.grid(row=0, column=0)
        
        self.ThirdCameraPos = Frame(self.SecondaryCamerasCont, bd=5, width=800, height=750, relief=RIDGE, bg='#1f1f1f')
        self.ThirdCameraPos.grid(row=1, column=0)
        
        self.FourthCameraPos = Frame(self.SecondaryCamerasCont, bd=5, width=800, height=750, relief=RIDGE, bg='#1f1f1f')
        self.FourthCameraPos.grid(row=2, column=0)
        
        self.FifthCameraPos = Frame(self.SecondaryCamerasCont, bd=5, width=800, height=750, relief=RIDGE, bg='#1f1f1f')
        self.FifthCameraPos.grid(row=3, column=0)
        
        #____________________________________________________BUTTONS___________________________________________________#
        
        self.SecondCameraButton = Button(self.SecondCameraPos, text="", bg='#1f1f1f', fg='white', command=lambda: self.change_pos(1))
        self.SecondCameraButton.grid(row=0, column=0, padx=5, pady=5)
        
        self.ThirdCameraButton = Button(self.ThirdCameraPos, text="", bg='#1f1f1f', fg='white', command=lambda: self.change_pos(2))
        self.ThirdCameraButton.grid(row=0, column=0, padx=5, pady=5)
        
        self.FourthCameraButton = Button(self.FourthCameraPos, text="", bg='#1f1f1f', fg='white', command=lambda: self.change_pos(3))
        self.FourthCameraButton.grid(row=0, column=0, padx=5, pady=5)
        
        self.FifthCameraButton = Button(self.FifthCameraPos, text="", bg='#1f1f1f', fg='white', command=lambda: self.change_pos(4))
        self.FifthCameraButton.grid(row=0, column=0, padx=5, pady=5)
        #_____________________________________________________IMAGE____________________________________________________#
        
        self.imagealarm = Image.open("C:\prctm_dog\images\siren.gif")
        self.imagealarm = self.imageFrame.resize((100, 100), Image.ANTIALIAS)
        self.imagealarm = ImageTk.PhotoImage(self.imagealarm)
        
        ImageOnMainCamera = Label(self.ImageOnMainCamera, image=self.imagealarm)
        ImageOnMainCamera.grid(row=0, column=0, padx=5, pady=5)
        
    #_____________________________________________________Defs____________________________________________________#
    
    def init_cameras(self):
        self.camera1 = camera_1.Camera_1(55)
        self.camera2 = camera_2.Camera_2(10)
        self.camera3 = camera_3.Camera_3(10)
        self.camera4 = camera_4.Camera_4(10)
        self.camera5 = camera_5.Camera_5(10)
        
    def change_pos(self, pos_changed):
        main_pos = 1
        sec_pos = pos_changed + 1
        
        #self.main_pos = positions[1]
        #changed_main_pos = positions[pos_changed + 1] #porque son arrs diferentes
        
        positions[main_pos], positions[sec_pos] = positions[sec_pos], positions[main_pos]
        
        self.main_pos = positions[1]
        self.changed_main_pos = positions[pos_changed + 1]
        self.sizes()
        self.camera_distr()
        
    def sizes(self):
        if self.main_pos == 1:
            self.focus_camera = 1
            camera_1.Camera_1(55)
            
            camera_2.Camera_2(10)
            camera_3.Camera_3(10)
            camera_4.Camera_4(10)
            camera_5.Camera_5(10)
        elif self.main_pos == 2:
            self.focus_camera = 2
            camera_2.Camera_2(55)
            
            camera_1.Camera_1(10)
            camera_3.Camera_3(10)
            camera_4.Camera_4(10)
            camera_5.Camera_5(10)
        elif self.main_pos == 3:
            self.focus_camera = 3
            camera_3.Camera_3(55)
            
            camera_1.Camera_1(10)
            camera_2.Camera_2(10)
            camera_4.Camera_4(10)
            camera_5.Camera_5(10)  
        elif self.main_pos == 4:
            self.focus_camera = 4
            camera_4.Camera_4(55)
            
            camera_1.Camera_1(10)
            camera_2.Camera_2(10)
            camera_3.Camera_3(10)
            camera_5.Camera_5(10)  
        elif self.main_pos == 5:
            self.focus_camera = 5
            camera_5.Camera_5(55)
            
            camera_1.Camera_1(10)
            camera_2.Camera_2(10)
            camera_3.Camera_3(10)
            camera_4.Camera_4(10)
            
    def camera_frames(self):   
        self.camera_frames = {  #la funcion definitiva
            1: self.ImageOnMainCamera,
            2: self.SecondCameraPos,
            3: self.ThirdCameraPos,
            4: self.FourthCameraPos,
            5: self.FifthCameraPos
        }
            
    def camera_distr(self): #si no funciona con image, quemar la escuela    //(probar con PIL)
        
        for visual_pos, cam_id in positions.items():    #position & camera frames
            frame = self.camera_frames[cam_id]  #de aqui accede a los diccionaarios
            if visual_pos == 1:
                frame.grid(row=0, column=1)
            elif visual_pos == 2:
                frame.grid(row=0, column=0)   
            elif visual_pos == 3:
                frame.grid(row=1, column=0)   
            elif visual_pos == 4:
                frame.grid(row=2, column=0)
            elif visual_pos == 5:
                frame.grid(row=3, column=0)
                    
        
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Camera_guy(root)
    root.mainloop()