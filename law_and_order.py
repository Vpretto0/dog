#GUI
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
        self.root.title(102 * titlespace + "THE LAW AND ORDER")
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
        
        self.lbltitle = Label(TitleFrame, font =('courier', 40, 'bold'),text ="The MATRIX DOG", bd =7)
        self.lbltitle.grid(row =0, column =0, padx =153)
        
        
        self.lblclass = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="Class", bd =7)
        self.lblclass.grid(row =1, column =0,sticky=W, padx =5 )
        self.entclass = Entry(LeftFrame1, font =('courier', 12, 'bold'),bd =5, width =44, justify = 'left')
        self.entclass.grid(row =1, column =1,sticky=W, padx =5 )
        
        self.lblID = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="ID", bd =7)
        self.lblID.grid(row =2, column =0,sticky=W, padx =5 )
        self.entID = Entry(LeftFrame1, font =('courier', 12, 'bold'),bd =5, width =44, justify = 'left')
        self.entID.grid(row =2, column =1,sticky=W, padx =5 )
        
        self.lblfirstname = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="First Name", bd =7)
        self.lblfirstname.grid(row =3, column =0,sticky=W, padx =5 )
        self.entfirstname = Entry(LeftFrame1, font =('courier', 12, 'bold'),bd =5, width =44, justify = 'left')
        self.entfirstname.grid(row =3, column =1,sticky=W, padx =5 )
        
        self.lbllastname = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="Last Name", bd =7)
        self.lbllastname.grid(row =4, column =0,sticky=W, padx =5 )
        self.entlastname = Entry(LeftFrame1, font =('courier', 12, 'bold'),bd =5, width =44, justify = 'left')
        self.entlastname.grid(row =4, column =1,sticky=W, padx =5 )
        
        self.lblmail = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="Mail", bd =7)
        self.lblmail.grid(row =5, column =0,sticky=W, padx =5 )
        self.txtmail = Entry(LeftFrame1, font =('courier', 12, 'bold'),bd =5, width =44, justify = 'left')
        self.txtmail.grid(row =5, column =1,sticky=W, padx =5 )
        
        self.lblphoto = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="Photo", bd =5)
        self.lblphoto.grid(row =6, column =0,sticky=W, padx =5 )
        self.cbophoto = ttk.Combobox(LeftFrame1, font =('courier', 12, 'bold'), width =42, state ='readonly')
        self.cbophoto['values'] = ('False', 'True')
        self.cbophoto.current(0)
        #Si es verdadero, que se abra una pestaña que muestre la foto, si es falso, que aparezca un boton con un texto que diga anadir foto
        self.cbophoto.grid(row =6, column =1,sticky=W, padx =5 )
        
        #___________________________________________________TABLE TREEVIEW____________________________________________________#
        
        scroll_y = Scrollbar(LeftFrame, orient = VERTICAL)
        self.people_records = ttk.Treeview(LeftFrame, height =14, columns =("class", "id", "name", "lastname", "mail", "photo"), yscrollcommand = scroll_y.set)
        scroll_y.pack(side =RIGHT, fill =Y)
        
        self.people_records.heading("class", text="Class")
        self.people_records.heading("id", text="ID")
        self.people_records.heading("name", text="First Name")
        self.people_records.heading("lastname", text="Last Name")
        self.people_records.heading("mail", text="Mail")
        self.people_records.heading("photo", text="Photo")
        
        self.people_records['show'] = 'headings'
        
        self.people_records.column("class", width= 70)
        self.people_records.column("id", width= 70)
        self.people_records.column("name", width= 100)
        self.people_records.column("lastname", width= 100)
        self.people_records.column("mail", width= 100)
        self.people_records.column("photo", width= 70)
        
        self.people_records.pack(fill =BOTH, expand =1)
        #___________________________________________________BUTTONS____________________________________________________#
        self.btnAddNew = Button(RightFrame1a, text = "Add New", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, bd =4). grid(row =0, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "Add New", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, bd =4). grid(row =1, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "Add New", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, bd =4). grid(row =2, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "Add New", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, bd =4). grid(row =3, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "Add New", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, bd =4). grid(row =4, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "Add New", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, bd =4). grid(row =5, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "Add New", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, bd =4). grid(row =6, column =0, padx =0)
        
        
        
        
if __name__=='__main__':
    root = Tk()
    aplication = law_and_order(root)
    root.mainloop()
