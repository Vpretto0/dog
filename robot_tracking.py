"""Archivo para ver las camaras del robot (deberian ser 5) y la rarita esa"""
import subprocess
import os
import sys
from PIL import Image, ImageTk

import ctypes
import time
import threading
import tkinter as tk 
from tkinter import *
from tkinter import ttk, messagebox
import pygame

user = "admin"
pswrd = "zmnta28fvcym"
init_cam = "python SPOT_cameras/live_feed_controls.py 192.168.80.3 --pixel-format PIXEL_FORMAT_GREYSCALE_U8 -j 100"
init_map = "python SPOT_gps/gps_listener.py 192.168.80.3"
init_wasd = "python SPOT_wasd/wasd.py 192.168.80.3"
init_estop = "python SPOT_estop/estop.py 192.168.80.3"

def start_with_the_password(init_cam, arg=None):
    args = init_cam.split()
    if arg:
        args += arg
    process = subprocess.Popen(     #POPEN
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    process.stdin.write(user + "\n")
    process.stdin.write(pswrd + "\n")
    process.stdin.flush()
    return process  #no alvidar return

class PygameEmbed:
        def __init__(self, parent, user, pswrd, init_cam):
            os.environ['SDL_WINDOWID'] = str(parent.winfo_id()) 
            if sys.platform == "win32": #no deberia causar problemas
                os.environ['SDL_VIDEODRIVER'] = 'windib'

            pygame.init()
            self.width = parent.winfo_width()
            self.height = parent.winfo_height()
            self.screen = pygame.display.set_mode((self.width, self.height))
            self.running = True
            self.username = user
            self.password = pswrd
            self.init_cam = init_cam
            
            screen = pygame.display.set_mode((800, 650))
            hwnd = pygame.display.get_wm_info()['window']
            ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)  # SWP_NOSIZE | SWP_NOMOVE
        
        def run(self):
            
            clock = pygame.time.Clock()
            font = pygame.font.SysFont(None, 28)
            # while self.running:
            #     for event in pygame.event.get():
            #         if event.type == pygame.QUIT:
            #             self.running = False
                # self.screen.fill((205, 160, 52))
                # user_text = font.render(f"Usuario: {self.username}", True, (255, 255, 255))
                # pass_text = font.render(f"Contraseña: {'*' * len(self.password)}", True, (255, 255, 255))
                # script_text = font.render(f"Script: {self.script_name}", True, (255, 255, 255))

                # self.screen.blit(user_text, (10, 10))     //Recordar cambiar esto pq lo quiero eliminar
                # self.screen.blit(pass_text, (10, 40))
                # self.screen.blit(script_text, (10, 70))
            #     pygame.display.flip()   #improvisar en el futuro
            #     clock.tick(30)  
            # pygame.quit()
            
def py_start(parent, username, password):
        pg = PygameEmbed(parent, init_cam, username, password)
        thread = threading.Thread(target=pg.run, daemon=True)
        thread.start()
        return pg, thread   #return

def toplv_cam( root, username, password):
    
    toplv = tk.Toplevel(root)
    toplv.title("Cámara")
    toplv.geometry("800x650+25+25")   #cambiar si no me gusta el tamano
    frame = Frame(toplv, bd=5, relief=RIDGE, width=800, height=650)
    frame.grid()
    
    MainCamFrame = Frame(frame, bd=5, relief=RIDGE, width=800, height=650)
    MainCamFrame.grid()
    
    CamFrame = Frame(MainCamFrame, bd=5, relief=RIDGE, width=800, height=650)
    CamFrame.grid(row=0, column=1)
    
    GifFrame = Frame(MainCamFrame, width=800, height=200)
    GifFrame.grid(row=0, column=0)
    
    gifile= "C:/prctm_dog/images/siren.gif"
    gif_image = tk.PhotoImage(file=gifile)
    
    gif_lbl = Label(GifFrame, bg='#1f1f1f')
    gif_lbl.grid()
    try:
        gif_image_temp = tk.PhotoImage(file=gifile, format="gif -index 0")
        total_frames = 0
        while True:
            tk.PhotoImage(file=gifile, format=f"gif -index {total_frames}")
            total_frames += 1
    except:
        pass
    gifimage_objects = [
        tk.PhotoImage(file=gifile, format=f"gif -index {i}")
        for i in range(total_frames)
    ]
        
    def animation(current_frame=0):
        image = gifimage_objects[current_frame]
        gif_lbl.configure(image=image)
        gif_lbl.image = image 

        next_frame = (current_frame + 1) % total_frames
        root.after(100, animation, next_frame)
    animation()
    toplv.update()
    
    pg_embed, _ = py_start(frame, username, password)
    
    def on_close():
        pg_embed.running = False
        time.sleep(0.3)
        toplv.destroy()
        
    toplv.protocol("WM_DELETE_WINDOW", on_close)
    time.sleep(0.3) 
    return toplv    #return

class tracking_robot:
    
    def __init__(self, root):
        self.root = root
        
        root.overrideredirect(True)
        #root.resizable(width=False, height=False)
        style = ttk.Style()
        style.theme_use('clam')
        root.configure(bg='#1f1f1f')
        
        self.mode = "Automatic Mode" #cambia
        
        #root.wm_attributes("-transparentcolor", "#1f1f1f" )
        
        self.root.attributes("-topmost", True)
        self.root.title("ROBOT TRACKING")
        self.root.geometry("800x750+25+25")
        
        self.estop_process = None
        
        
        #____________________________________________________TK(?)___________________________________________________#
        #1080
        #CAMBIAR ESTO A TRANSPARENTE
        MainFrame = Frame(self.root, bd=5, width=925, height=750, relief=RIDGE, bg='#1f1f1f') #quitar al final
        MainFrame.grid()
        
        NotifFrame = Frame(MainFrame, bd=5, width=100, height=250, relief=RIDGE, bg='#1f1f1f')
        NotifFrame.grid(pady=20)
        CaptureFrame = Frame(MainFrame, bd=5, width=100, height=250, relief=RIDGE, bg='#1f1f1f')
        CaptureFrame.grid(pady=20)
        BackBtnFrame = Frame(MainFrame, bd=5, width=600, height=250, relief=RIDGE, bg='#1f1f1f')
        BackBtnFrame.grid(pady=20)

        CamFrame = Frame(MainFrame, bd=5, width=800, height=650, relief=RIDGE, bg='#1f1f1f')
        CamFrame.grid(row=0, column=0)
        ButtonsFrame = Frame(MainFrame, bd=5, width=800, height=250, relief=RIDGE, bg='#1f1f1f')
        ButtonsFrame.grid(row=1, column=0)
        
        LeftFrame = Frame(MainFrame, bd=5, width=800, height=800, relief=RIDGE, bg='#1f1f1f')
        LeftFrame.grid(row=0, column=0)
        SpaceFrame = Frame(LeftFrame, width=300, height=800)
        SpaceFrame.grid(row=0, column=1)
        RightFrame = Frame(MainFrame, bd=5, width=640, height=800, relief=RIDGE, bg='#1f1f1f')
        RightFrame.grid(row=0, column=2)
        
        DVerificatioFrame = Frame(RightFrame, bd=5, width=640, height=290, relief=RIDGE, bg='#1f1f1f')
        DVerificatioFrame.grid(column=0, row=0)
        SpotUtilitiesFrame = Frame(RightFrame, bd=5, width=400, height=400, relief=RIDGE, bg='#1f1f1f')
        SpotUtilitiesFrame.grid(column=0, row=1)
        
        MapFrame = Frame(RightFrame, bd=5, width=350, height=400, relief=RIDGE, bg='#1f1f1f')
        MapFrame.grid(column=0, row=1)
        SpotEtcFrame = Frame(RightFrame, bd=5, width=290, height=400, relief=RIDGE, bg='#1f1f1f')
        SpotEtcFrame.grid(column=1, row=1)
        
        eStopFrame = Frame(MainFrame, bd=5, width=290, height=250, relief=RIDGE, bg='#1f1f1f')
        eStopFrame.grid(pady=20)
        SwitchFrame = Frame(MainFrame, bd=5, width=290, height=150, relief=RIDGE, bg='#1f1f1f')
        SwitchFrame.grid(pady=20)
        
        self.btn_mode = Button(MainFrame, text=self.mode, command=self.button_manual_auto, bg="#444", fg="white", width=15)
        self.btn_mode.grid(pady=10)    
        
        
        
        #self.start(command, user, pswrd, arg=None)
        toplv_cam(self.root, user, pswrd)

        
    #____________________________________________________FUNCTIONS___________________________________________________#
        
    def start(self, command, user, pswrd, arg=None):
        try:
            return start_with_the_password(command, user, pswrd, arg)
        except Exception as e:
            print(f"Error al iniciar script {command}: {e}")
            return None
            
    def wasd_button(self):
        messagebox.showinfo("Manual Mode", "Controls: \nW = Forward\nS = Backward\nA = Left\nD - Right\nQ = Turn Left\nE = Turn Right")
        messagebox.showinfo("Manual Mode", "Commands: \nTAB = Quit\nT = Time-sync\nSPACE = Estop\nP = Power\nI = Take Image\nO = Video mode\nf = Stand\nr = Self-right\nv = Sit\nb = Battery-change\nESC = Stop\n1 = Return/Acquire Lease")
        import SPOT_wasd as Wasd
        Wasd.wasd(self.root)
    
    
    #VER COMO ADAPTAR EL TAMANO DEL ESTOP EN EL RAW
    def open_estop(self):
        estop_frame = Frame(self.root, bd=5, width=500, height=500, relief=RIDGE, bg='#1f1f1f')
        estop_frame.grid(pady=20)
        self.run_estop()

    def run_estop(self):
        if self.estop_process is None:
            self.estop_process = subprocess.Popen(['python', 'SPOT_estop/estop.py', '192.168.80.3'],
                                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE, text=True)
            print("eStarted")
        else:
            print("eDoesntWork")
            
    def auto_mode(self):
        pass            
    
    #WASD CONTROLLS
    #VER COMO PROGRAMAR ESO
    def manual_mode(self):
        pass
    
    def button_manual_auto(self):
        if self.mode == "Automatic Mode":
            self.mode = "Manual Mode"
            self.btn_mode.config(text=self.mode)
            #self.manual_mode()
            self.wasd_button()
        else:
            self.mode = "Automatic Mode"
            self.btn_mode.config(text=self.mode)
            self.auto_mode()
            
    #GPS MAP
    def start_map(self):
        pass
            
        
if __name__ == "__main__":
    root = Tk()
    app = tracking_robot(root)
    root.mainloop()