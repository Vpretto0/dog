from tkinter import *
import time
import tkinter as tk
from tkinter import ttk, Tk
from PIL import Image, ImageTk, ImageGrab
import os

from verification_tracking import db_verification

class tracking_main:
    
    def __init__(self, root):
        #Init Camera=
        self.root = root
        
        root.overrideredirect(True)
        root.resizable(width=False, height=False)
        style = ttk.Style()
        style.theme_use('clam')
        root.configure(bg='#1f1f1f')
        
        root.wm_attributes("-transparentcolor", "green")
        
        self.root.attributes("-topmost", True)
        self.root.title("MATRIX DOG")
        self.root.geometry("1425x700+75+55")

        root.update_idletasks()  #("Hack")  
        
        # x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        # y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        # root.geometry("+%d+%d" % (x, y))
        
        self.mode = "Automatic Mode"
        
        #TopLevel
        def DB_verification():
                db_window = Toplevel(self.root) 
                self.pw = db_verification(db_window)
        DB_verification()
        
        #____________________________________________________FRAMES___________________________________________________#

        MainFrame = Frame(self.root, width=1450, height=700, bg='green')        #ya
        MainFrame.grid()
        
        LeftFrame = Frame(MainFrame, width=770, height=690, bg='green')
        LeftFrame.grid(row=0, column=0)
        RightFrame = Frame(MainFrame, width=670, height=690, bg='green')
        RightFrame.grid(row=0, column=1)
        
    #Right Stuff=
        verificationdbFrame = Frame(RightFrame, width=670, height=345, bg='green')
        verificationdbFrame.grid(row=0, column=0)
        
        downRStuffFrame = Frame(RightFrame, width=670, height=345, bg='green')
        downRStuffFrame.grid(row=1, column=0)
    
        MapFrame = Frame(downRStuffFrame, width=342, height=345, bg='darkblue')
        MapFrame.grid(row=0, column=0)
        ButtonsFrame = Frame(downRStuffFrame, width=338, height=345, bg='green')
        ButtonsFrame.grid(row=0, column=1)
        
        eStopButtonFrame = Frame(ButtonsFrame, width=338, height=230, bg='green')
        eStopButtonFrame.grid(row=0, column=0)
        SwitchButtonFrame = Frame(ButtonsFrame, width=338, height=115, bg='green')
        SwitchButtonFrame.grid(row=1, column=0)
        
    #Left Stuff=
        GifFrame = Frame(LeftFrame, width=765, height=180, bg='green')
        GifFrame.grid(row=0, column=0)
        CameraFrame = Frame(LeftFrame, width=765, height=420, bg='darkred')
        CameraFrame.grid(row=1, column=0)
        downLStuffFrame = Frame(LeftFrame, width=765, height=90, bg='green')
        downLStuffFrame.grid(row=2, column=0)
        
        #_____________________________________________________BUTTONS___________________________________________________#
        
    #Left Buttons=
        BackButton = Button(downLStuffFrame, bd=5, relief=RIDGE, text="GO BACK", width=85, height=2, fg='white', bg = '#212121', activebackground='gray', command=self.back)
        BackButton.grid(row=0, column=0, padx=5, pady=20)
        
        self.NotificationImg= PhotoImage(file="C:/prctm_dog/images/notification_icon.png") 
        NotificationButton = Button(downLStuffFrame, bd=5, relief=RIDGE, image=self.NotificationImg, width=35, height=35, fg='white', bg = '#212121', activebackground='gray')
        NotificationButton.grid(row=0, column=1, padx=5, pady=15)
        
        self.CameraImg= PhotoImage(file="C:/prctm_dog/images/camera_icon.png") 
        captureButton = Button(downLStuffFrame, bd=5, relief=RIDGE, image=self.CameraImg, width=35, height=35, fg='white', bg = '#212121', activebackground='gray')
        captureButton.grid(row=0, column=2, padx=5, pady=15)
        
    #Right Buttons=
        self.e_path= PhotoImage(file="C:/prctm_dog/images/estop.png") 
        eStopButton = Button(eStopButtonFrame, image=self.e_path, fg='green', bg = 'green', activebackground='green', borderwidth=0, cursor='hand2')
        eStopButton.grid(row=0, column=0, padx=6, pady=6)
         
        self.SwitchButton = Button(SwitchButtonFrame, bd=10, width=25, height=3, relief=RIDGE, text=self.mode, font =('courier', 10, 'bold'), command=self.button_manual_auto, fg='white', bg = '#212121', activebackground='gray')
        self.SwitchButton.grid(row=0, column=0, padx=10, pady=20)
    
    #GIF=
        GifFrame = Frame(GifFrame, width=800, height=200, bg="green")
        GifFrame.grid(row=0, column=0)
        
        gifile= "C:/prctm_dog/images/siren.gif"
        
        gif_lbl = Label(GifFrame, bg="green") 
        gif_lbl.grid()
        
        total_frames = 0
        gifimage_objects = []
        while True:
            try:
                frame = PhotoImage(file=gifile, format=f"gif -index {total_frames}")
                gifimage_objects.append(frame)
                total_frames += 1
            except:
                break
            
        def animation(current_frame=0):
            image = gifimage_objects[current_frame]
            gif_lbl.configure(image=image)
            gif_lbl.image = image 

            next_frame = (current_frame + 1) % total_frames #a %
            root.after(100, animation, next_frame)
        animation()
        #____________________________________________________FUNCTIONS___________________________________________________#
        
#Switch Button=
    def button_manual_auto(self):
        if self.mode == "Automatic Mode":
            self.mode = "Manual Mode"
            self.SwitchButton.config(text=self.mode)
            #self.manual_mode()
            print("Manual Mode")
        else:
            self.mode = "Automatic Mode"
            self.SwitchButton.config(text=self.mode)
            print("Automatic Mode")
            
#Back Button=
    def back(self):
        self.root.withdraw()
        try:
            os.system('.venv/Scripts/activate')
        except Exception:
            pass
        finally:
            self.root.after(1000)
            self.root.destroy()
            os.system('python C:\prctm_dog\start_menu.py')
        
# #Screenshot Button=
#     def save_as_png(self):
#         self.file = "C:/prctm_dog/security_picture.png"
#         ImageGrab.grab().crop((713, 168, 1210, 915)).save(self.file)

#         self.root.after(2000)
#         label = Label(self.CamLavel, text="DATA SAVED...", font =('courier', 15, 'bold'), fg='#1f1f1f', bg='black', bd=5, relief=RIDGE)
#         label.grid()
#         label.update_idletasks() 
        
#         label.after(2000, label.destroy)
#         #RECORDAR SUMER LOS TIEMPOS

#WASD=
    def wasd(self):
        self.root.withdraw()
        self.root.after(1000)
        self.root.destroy()
        os.system('python C:\prctm_dog\main_tracking.py')

            
if __name__ == "__main__":
    root = Tk()
    app = tracking_main(root)
    
    root.mainloop()