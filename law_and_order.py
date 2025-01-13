#GUI(basically)
import db_identity
import qr_generation
import qr_indentification

from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import pymysql


class law_and_order:
    
    def __init__(self, root):
        
        self.root = root
        titlespace = " "
        self.root.title(102 * titlespace + "Dog for the Law and Order")
        self.root.geometry("800x700+50+50") # width x height + X coordinate + Y coordinate
        self.root.resizable(width =False, height =False)
        
        MainFrame = Frame(self.root, bd =10, width =770, height =700, relief = RIDGE, bg = '#1f1f1f')
        MainFrame.grid()
        
        TitleFrame = Frame(MainFrame, bd =7, width =770, height =100, relief = RIDGE)
        TitleFrame.grid(row =0, column =0)
        TopFrame3 = Frame(MainFrame, bd =5, width =770, height =500, relief = RIDGE)
        TopFrame3.grid(row =1, column =0)
        
        LeftFrame = Frame(TopFrame3, bd =5, width =770, height =400,padx =2, relief = RIDGE, bg = '#1f1f1f')
        LeftFrame.pack(side =LEFT)
        LeftFrame1 = Frame(LeftFrame, bd =5, width =600, height =180,padx =2, pady =4, relief = RIDGE)
        LeftFrame1.pack(side =TOP, padx =0, pady =0)
        
        RightFrame1 = Frame(TopFrame3, bd =5, width =100, height =400,padx =2, relief = RIDGE, bg = '#1f1f1f')
        RightFrame1.pack(side =RIGHT)
        RightFrame1a = Frame(RightFrame1, bd =5, width =90, height =300,padx =2, pady =2, relief = RIDGE)
        RightFrame1a.pack(side =TOP, padx =0, pady =0)
        #_______________________________________________________________________________________________________#
        
        self.lbltitle = Label(TitleFrame, font ='Courier New'), "The MATRIX"
        
        
        
if __name__=='__main__':
    root = Tk()
    aplication = law_and_order(root)
    root.mainloop()
