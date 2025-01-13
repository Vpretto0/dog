#GUI
import db_identity
from db_identity import *
import qr_generation
import qr_indentification

from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import pymysql


class law_and_order:
    
    def __init__(self, root):
        #editar la parte de arriba, para que solo se vea el titulo y ajustar las posiciones y loas tamaños correctos
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
        Class = StringVar()
        pid = IntVar()
        name = StringVar()
        lastname = StringVar()
        mail = StringVar()
        photo = BooleanVar()
        
        #———————————————————————————————————————————————————————————————————————————————————————————————————————#
        
        def iExit():
            iExit = tkinter.messagebox.askyesno("THE LAW AND ORDER", "Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return
        
        def Reset():
            self.entclass.delete(0, END)
            self.entID.delete(0, END)
            self.entfirstname.delete(0, END)
            self.entlastname.delete(0, END)
            self.entmail.delete(0, END)
            photo.set("False")
            
            
        def addData():
            if pid.get() == "" or name.get() == "" or lastname.get() == "":
                tkinter.messagebox.showerror("THE LAW AND ORDER", "Enter Correct Details.\n\n    don't be stupid")
                
            else: 
                conn, c  = db_identity.create_connection()
                if conn is not None and c is not None:
                    c.execute("INSERT INTO people VALUES (%s, %s, %s, %s, %s, %s)", (Class.get(), pid.get(), name.get(), lastname.get(), mail.get(), photo.get()))
                    conn.commit()
                    db_identity.close_connection(conn, c)
                    tkinter.messagebox.showinfo("THE LAW AND ORDER", "Record Entered Successfully")
                    #arreglado
                else:
                    tkinter.messagebox.showerror("THE LAW AND ORDER", "Error Entering to database")
                    #super dificil de arreglar
            
        #_______________________________________________________________________________________________________#
        
        self.lbltitle = Label(TitleFrame, font =('courier', 40, 'bold'),text ="The MATRIX DOG", bd =7)
        self.lbltitle.grid(row =0, column =0, padx =153)
        
        
        self.lblclass = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="Class", bd =7)
        self.lblclass.grid(row =1, column =0,sticky=W, padx =5 )
        self.entclass = Entry(LeftFrame1, font =('courier', 12, 'bold'),bd =5, width =44, justify = 'left', textvariable= Class)
        self.entclass.grid(row =1, column =1,sticky=W, padx =5 )
        
        self.lblID = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="ID", bd =7)
        self.lblID.grid(row =2, column =0,sticky=W, padx =5 )
        self.entID = Entry(LeftFrame1, font =('courier', 12, 'bold'),bd =5, width =44, justify = 'left', textvariable= pid)
        self.entID.grid(row =2, column =1,sticky=W, padx =5 )
        
        self.lblfirstname = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="First Name", bd =7)
        self.lblfirstname.grid(row =3, column =0,sticky=W, padx =5 )
        self.entfirstname = Entry(LeftFrame1, font =('courier', 12, 'bold'),bd =5, width =44, justify = 'left', textvariable= name)
        self.entfirstname.grid(row =3, column =1,sticky=W, padx =5 )
        
        self.lbllastname = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="Last Name", bd =7)
        self.lbllastname.grid(row =4, column =0,sticky=W, padx =5 )
        self.entlastname = Entry(LeftFrame1, font =('courier', 12, 'bold'),bd =5, width =44, justify = 'left', textvariable= lastname)
        self.entlastname.grid(row =4, column =1,sticky=W, padx =5 )
        
        self.lblmail = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="Mail", bd =7)
        self.lblmail.grid(row =5, column =0,sticky=W, padx =5 )
        self.entmail = Entry(LeftFrame1, font =('courier', 12, 'bold'),bd =5, width =44, justify = 'left', textvariable= mail)
        self.entmail.grid(row =5, column =1,sticky=W, padx =5 )
        
        self.lblphoto = Label(LeftFrame1, font =('courier', 12, 'bold'),text ="Photo", bd =5)
        self.lblphoto.grid(row =6, column =0,sticky=W, padx =5 )
        self.cbophoto = ttk.Combobox(LeftFrame1, font =('courier', 12, 'bold'), width =42, state ='readonly', textvariable = photo)
        self.cbophoto['values'] = ('False', 'True')
        self.cbophoto.current(0)
        #Si es verdadero, que se abra una pestaña que muestre la foto, si es falso, que aparezca un boton con un texto que diga anadir foto
        self.cbophoto.grid(row =6, column =1,sticky=W, padx =5 )
        
        #___________________________________________________TABLE TREEVIEW____________________________________________________#
        
        scroll_y = Scrollbar(LeftFrame, orient = VERTICAL)
        self.people_records = ttk.Treeview(LeftFrame, height =14, columns =("class", "pid", "name", "lastname", "mail", "photo"), yscrollcommand = scroll_y.set)
        scroll_y.pack(side =RIGHT, fill =Y)
        
        self.people_records.heading("class", text="Class")
        self.people_records.heading("pid", text="ID")
        self.people_records.heading("name", text="First Name")
        self.people_records.heading("lastname", text="Last Name")
        self.people_records.heading("mail", text="Mail")
        self.people_records.heading("photo", text="Photo")
        
        self.people_records['show'] = 'headings'
        
        self.people_records.column("class", width= 70)
        self.people_records.column("pid", width= 70)
        self.people_records.column("name", width= 100)
        self.people_records.column("lastname", width= 100)
        self.people_records.column("mail", width= 100)
        self.people_records.column("photo", width= 70)
        
        self.people_records.pack(fill =BOTH, expand =1)
        #___________________________________________________BUTTONS____________________________________________________#
        self.btnAddNew = Button(RightFrame1a, text = "Add Data", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2,command =addData, bd =4). grid(row =0, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "Display", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, bd =4). grid(row =1, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "Update", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, bd =4). grid(row =2, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "Delete", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, bd =4). grid(row =3, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "Search", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, bd =4). grid(row =4, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "Reset", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, command =Reset,  bd =4). grid(row =5, column =0, padx =0)
        
        self.btnAddNew = Button(RightFrame1a, text = "EXIT", font =('courier', 14, 'bold'),
            padx =15, pady=2, width =8, height =2, command =iExit, bd =4). grid(row =6, column =0, padx =0)
        
        
        
        
if __name__=='__main__':
    root = Tk()
    aplication = law_and_order(root)
    root.mainloop()
    
    
# conseguir la informacion de todos los estudiantes de la clase e ingresarla en la base de datos
