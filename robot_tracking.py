#Archivo para ver las camaras del robot (deberian ser 5) y la rarita esa
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import SPOT_cameras.GUI_cameras as GUY

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
        
        #____________________________________________________TK(?)___________________________________________________#
    
        MainFrame = Frame(self.root, bd=5, width=925, height=750, relief=RIDGE, bg='#1f1f1f') #quitar al final
        MainFrame.grid()


        self.btn_mode = Button(MainFrame, text=self.mode, command=self.button_manual_auto, bg="#444", fg="white", width=15)
        self.btn_mode.pack(pady=10)
        
    #____________________________________________________FUNCTIONS___________________________________________________#

    def vigilance_guy(self):
            GUY.Camera_guy(self.root)
            #??? no se, me da pereza
    vigilance_guy()
        
    def wasd_button(self):
        messagebox.showinfo("Manual Mode", "Controls: \nW = Forward\nS = Backward\nA = Left\nD - Right\nQ = Turn Left\nE = Turn Right")
        messagebox.showinfo("Manual Mode", "Commands: \nTAB = Quit\nT = Time-sync\nSPACE = Estop\nP = Power\nI = Take Image\nO = Video mode\nf = Stand\nr = Self-right\nv = Sit\nb = Battery-change\nESC = Stop\n1 = Return/Acquire Lease")
        import SPOT_wasd as Wasd
        Wasd.wasd(self.root)
        
    def auto_mode(self):
        pass            
    
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
            
        
if __name__ == "__main__":
    root = tk.Tk()
    app = tracking_robot(root)
    root.mainloop()