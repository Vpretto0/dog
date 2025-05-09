from tkinter import ttk
from tkinter import *
import tkinter.messagebox

import law_and_order
#import verification_tracking

from PIL import Image, ImageTk


class menu_start:

    def __init__(self, root):
        
        root.overrideredirect(True)
        style = ttk.Style()
        style.theme_use('clam')
        
        self.root = root 
        self.root.resizable(width =False, height =False)
        self.root.configure(bg = '#1f1f1f') 
        
        root.attributes("-topmost", True)
        
        root.withdraw()
        root.update_idletasks()#Hack

        root.deiconify()
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        x = (screen_width - 773) // 2
        y = (screen_height - 494) // 2
        self.root.geometry("%dx%d+%d+%d" % (773, 494, x, y))
        #_______________________________________________EMPTY FRAMES________________________________________________#
        MainFrame = Frame(self.root, bd =10, width =750, height =550, relief = RIDGE, bg = '#1f1f1f')
        MainFrame.grid()
        
        
        TitleFrame = Frame(MainFrame, width =745, height =50, bg = '#1f1f1f')
        TitleFrame.grid()
        
        SubtitleFrame = Frame(MainFrame, width =745, height =5, bg = '#1f1f1f')
        SubtitleFrame.grid(row =1, column =0)
        
        ContentFrame = Frame(MainFrame, width =730, height =300, bg = '#1f1f1f')
        ContentFrame.grid(row =2, column =0)
        
        ImageFrame = Frame(ContentFrame, bd =5, width = 445, height =300, relief = RIDGE, bg = 'black')
        ImageFrame.grid(row =0, column =2, padx=10)
        
        SpaceContentFrame = Frame(ContentFrame, width =35, height =293, relief=RIDGE , bg = '#1f1f1f')
        SpaceContentFrame.grid(row =0, column =1)
        
        ButtonFrame = Frame(ContentFrame, width =300, height =300, bg = '#1f1f1f')
        ButtonFrame.grid(row =0, column =0)
        
        InteractableFrame = Frame(MainFrame, width =700, height =70, bg = '#1f1f1f')
        InteractableFrame.grid(row =3, column =0)
        
        TrackingFrame = Frame(InteractableFrame, bd =5, width =300, height =60, relief = RIDGE, bg = 'white')
        TrackingFrame.grid(row =0, column =0)
        
        HelpFrame = Frame(InteractableFrame, width =145, height =60, bg = '#1f1f1f')
        HelpFrame.grid(row =0, column =1)
        
        DBFrame = Frame(InteractableFrame, bd =5, width =300, height =60, relief = RIDGE, bg = 'white')
        DBFrame.grid(row =0, column =2)
   
        #__________________________________________________FRAMES___________________________________________________#
        self.lbltitle = Label(TitleFrame, font=('Courier', 40, 'bold'), text="The MATRIX DOG", fg='white', bg='#1f1f1f')
        self.lbltitle.grid(row=0, column=0)
        self.lblsubtitle = Label(SubtitleFrame, font=('Courier', 11, 'bold'), text="THE MOST SECURE APP IN THE WORLD SINCE YEAR 0000 0001", fg='white', bg='#1f1f1f')
        self.lblsubtitle.grid(row=0, column=0)
        
        self.btnAddNew = Button(ButtonFrame, text = "Options", font =('courier', 12, 'bold'), fg='white', bg = '#212121', activebackground='gray', relief=RIDGE, command=self.options,
            padx =40, pady=2, width =10, height =0, bd=5). grid(row =0, column =0, padx =15, pady=4, sticky='ew')
        
        self.btnAddNew = Button(ButtonFrame, text = "Language", font =('courier', 12, 'bold'), fg='white', bg = '#212121', activebackground='gray', relief=RIDGE, command=self.language,
            padx =50, pady=2, width =10, height =0, bd=5). grid(row =1, column =0, padx =15, pady=10, sticky='ew')
        
        self.btnAddNew = Button(ButtonFrame, text = "EXIT", font =('courier', 14, 'bold'), fg = "red", bg = '#212121', activebackground='gray', relief=RIDGE, command=self.iExit,
            padx =40, pady=5, width =10, height =0, bd =5). grid(row =2, column =0, padx =15, pady=4, sticky='ew')
        
        self.lblinvisible = Label(ButtonFrame, font=('Courier', 14, 'bold'), text=" ", fg='#1f1f1f', bg='#1f1f1f', anchor="w", width=15). grid(row=3, column=0, sticky='ew', padx=0, pady=0)
        
        
        self.police_image = "images/police_dog002.jpg"
        self.image_police = Image.open(self.police_image)
        self.image_police = self.image_police.resize((440, 245))
        self.image_police = ImageTk.PhotoImage(self.image_police)
        self.lblimage = Label(ImageFrame, image=self.image_police, bg='#1f1f1f')
        self.lblimage.grid(row=0, column=0)
        
        self.image_path= PhotoImage(file="C:/prctm_dog/images/info-24.png") 
        self.btnChange= Button(HelpFrame,text= "click", image=self.image_path, bg= '#1f1f1f', fg= 'green', borderwidth=0, activebackground='#212121', cursor='hand2').grid(row=0, column=0, padx=25, pady=20)
        
        self.btnAddNew = Button(TrackingFrame, text = "ROBOT TRACKING", font =('courier', 14, 'bold'), fg='white', bg = '#212121', activebackground='gray', relief=RIDGE, command=self.verification_tracking_function,
            padx =0, pady=0, width =25, height =0, bd=5). grid(row =0, column =0, sticky='ew')
        
        self.btnAddNew = Button(DBFrame, text = "DATA BASE", font =('courier', 14, 'bold'), fg='white', bg = '#212121', activebackground='gray', relief=RIDGE, command=self.law_and_order_function,
            padx =0, pady=0, width =25, height =0, bd=5). grid(row =0, column =0, sticky='ew')

    #___________________________________________________VARIABLES____________________________________________________#
    
    def iExit(self):
        self.iExit = tkinter.messagebox.askyesno("MATRIX DOG", "Confirm if you want to exit")
        if self.iExit > 0:
            self.root.destroy()
            return
        
    def options(self):
        self.iExit = tkinter.messagebox.showinfo("MATRIX DOG", "No options, \nbut I want some money")
        return
        
    def language(self):
        self.iExit = tkinter.messagebox.showinfo("MATRIX DOG", "Why you do want to change the Language?\n\nYou can speak English")
        return
    
    def law_and_order_function(self):
        law = Toplevel(self.root) 
        law.law_and_order = law_and_order.law_and_order(law)
        self.root.withdraw()
        
        #y ahora que?
        
    def verification_tracking_function(self):
        pass
        # verif = Toplevel(self.root)
        # verif.verification_tracking = verification_tracking.db_verification(verif)
        # self.root.withdraw()
        
       
        
if __name__=='__main__':
    root = Tk()
    aplication = menu_start(root)
    root.mainloop()