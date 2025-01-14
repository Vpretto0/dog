
from tkinter import ttk
from tkinter import *

def photo_run():
    print("running from photo.py")
    
class photo_class:
    
    def __init__(self, root):
        
        #root.overrideredirect(True)
        style = ttk.Style()
        style.theme_use('clam')
        
        
        root.configure(bg='#f1f1f1')
        self.root = root
        titlespace = " "
        self.root.title(102 * titlespace + "Photo Frame")
        self.root.geometry("235x380+850+350") # width x height + X coordinate + Y coordinate
        self.root.resizable(width =False, height =False)
        self.root.configure(bg = '#1f1f1f')
        
        MainFrame = Frame(self.root, bd =10, width =225, height =270, relief = RIDGE, bg = '#1f1f1f')
        MainFrame.grid()
        
        TitleFrame = Frame(MainFrame, bd =7, width =215, height =25, relief = RIDGE, bg = '#1f1f1f')
        TitleFrame.grid(row =0, column =0)
        TopFrame3 = Frame(MainFrame, bd =5, width =215, height =245, relief = RIDGE, bg = '#1f1f1f')
        TopFrame3.grid(row =1, column =0)
        
        # LeftFrame = Frame(TopFrame3, bd =5, width =215, height=27,padx =2, relief = RIDGE, bg = '#1f1f1f')
        # LeftFrame.pack(side =LEFT)
        TopFrame = Frame(TopFrame3, bd =5, width =205, height =228,padx =2, pady =4, bg = '#1f1f1f')
        TopFrame.pack(side =TOP, padx =0, pady =0)
        BottomFrame = Frame(TopFrame3, bd =7, width =205, height =45,padx =2, pady =4, bg = '#1f1f1f')
        BottomFrame.pack(side =BOTTOM, padx =0, pady =0)
        #_______________________________________________________________________________________________________#
        
        self.lbltitle = Label(TitleFrame, font =('courier', 16, 'bold'),text ="PHOTO", bd =5, fg='white', bg='#1f1f1f')
        self.lbltitle.grid(row =0, column =0, padx =62)
        #_______________________________________________________________________________________________________#
        
            #182x228y
        photo = Frame(TopFrame, bd =7, width =182, height =228,relief= RIDGE, bg = '#1f1f1f')
        photo.pack()
        
        
        def show_image():
            pass
            
        
        #_______________________________________________________________________________________________________#
        
        self.btnAddNew = Button(BottomFrame, text = "Change", font =('courier', 10, 'bold'), fg='white', bg = '#212121', activebackground='gray',
            padx =5, pady=1, width =8, height =1,  bd =5). grid(row =0, column =0, padx =3)
        
        self.btnAddNew = Button(BottomFrame, text = "DELETE", font =('courier', 10, 'bold'), fg = "red", bg = '#212121', activebackground='red',
            padx =5, pady=1, width =8, height =1, bd =5). grid(row =0, column =1, padx =3)
        #_______________________________________________________________________________________________________#
        
        
if __name__=='__main__':
    root = Tk()
    aplication = photo_class(root)
    root.mainloop()