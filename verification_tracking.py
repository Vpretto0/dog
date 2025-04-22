#Archivo para poder ver la base de datos que registra los ids
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

import db_identity_verification
from robot_tracking import tracking_robot

class db_verification:
    
    def __init__(self, root):
        self.root = root
        
        root.overrideredirect(True)
        root.resizable(width=False, height=False)
        style = ttk.Style()
        style.theme_use('clam')
        root.configure(bg='#1f1f1f')
        
        #root.attributes("-alpha", 0.5)         //future*
        
        self.root.attributes("-topmost", True)
        self.root.title("MATRIX DOG - ROBOT TRACKING VERIFICTION OF DB")
        self.root.geometry("650x290+850+65")
        
        #____________________________________________________FRAMES___________________________________________________#
        
        MainFrame = Frame(self.root, bd=5, width=640, height=290, relief=RIDGE, bg='#1f1f1f')
        MainFrame.grid()
        
        
        #____________________________________________________FUNCTIONS___________________________________________________#
        
        datetime = StringVar()
        ipv6 = StringVar()
        Pass = BooleanVar()
        Class = StringVar()
        info = IntVar()
        idii = StringVar()
    
        def traineeinfo(ev):  # la funcion mas profesional de todas

            viewInfo = self.people_records.focus()
            learnerData = self.people_records.item(viewInfo)
            row = learnerData['values']
            datetime.set(row[0])
            ipv6.set(row[1])
            Pass.set(row[2])
            Class.set(row[3])
            info.set(row[4])
            idii.set(row[5])
            
        def DisplayData():
            print("starting display data")
            try:
                connn, cc  = db_identity_verification.create_connection()
                if connn is not None and cc is not None:
                    cc.execute("SELECT * FROM `verification`") #si da error eliminar *
                    
                    result = cc.fetchall()
                    print(f"Fetched {len(result)} records")
                    
                    if len(result) !=0:
                        self.people_records.delete(*self.people_records.get_children())
                        result = result[::-1]   #result.reverse() //es el comando mas imporsible de encontrar de mundo
                        
                        for row in result:
                            highlighting_invalids(row)
                    else:
                        print("No data")
                            
                else:
                    messagebox.showerror("THE LAW AND ORDER", "Error Entering to database")
                    #super dificil de arreglar
            except Exception as e:
                print(f"Error: {e}")
            
            finally:
                db_identity_verification.close_connection(connn, cc)
                self.people_records.after(3000, DisplayData)
                
        def highlighting_invalids(row):
            
            class_class = row[3]
            CAPTCHA = self.people_records.insert("", END, values=row)
            
            if class_class == "invalid":
                self.people_records.item(CAPTCHA, tags=('invalid',))
            elif class_class == "staff":
                self.people_records.item(CAPTCHA, tags=('staff',))
            elif class_class == "FBI":
                self.people_records.item(CAPTCHA, tags=('FBI',))
                
            self.people_records.tag_configure('staff', background='#2e2e2e')
            self.people_records.tag_configure('invalid', background='#1c0f0f', foreground='red')
            self.people_records.tag_configure('FBI', background='#0f101c', foreground='blue')      
            
        def robot_trk():
            tracking_cam = Toplevel(self.root) 
            self.trk = tracking_robot(tracking_cam)
        robot_trk()
        #______________________________________________VERIFICATION FRAME______________________________________________#
        
        scroll_y = Scrollbar(MainFrame, orient = VERTICAL, bg='#1f1f1f')
        self.people_records = ttk.Treeview(MainFrame, height =10, columns =("datetime", "ipv6", "Pass", "Class", "info", "idii"), yscrollcommand = scroll_y.set) #, "Pass"
        scroll_y.pack(side =RIGHT, fill =Y)
        
        style = ttk.Style()
        style.configure('Custom.TCombobox', fieldbackground='black', background='white', foreground='white', selectbackground='black', selectforeground='white')
        style.configure("Treeview", background="#1f1f1f", foreground="white", rowheight=25, fieldbackground="#1f1f1f")
        style.map("Treeview", background=[('selected', 'black')], foreground=[('selected', 'gray')])
        style.map( 'Custom.TCombobox', fieldbackground=[('readonly', 'black')], foreground=[('readonly', 'white')], background=[('active', 'black')])
        style.configure("Treeview.Heading", background='#1f1f1f', foreground="gray", font=('courier', 12, 'bold'))
        
        self.people_records.heading("datetime", text="datetime")
        self.people_records.heading("ipv6", text="IPv6 Adress")
        self.people_records.heading("Pass", text="")
        self.people_records.heading("Class", text="Class")
        self.people_records.heading("info", text="Info")
        self.people_records.heading("idii", text="ID")
        
        self.people_records['show'] = 'headings'
        
        self.people_records.column("datetime", width= 160, anchor=CENTER)
        self.people_records.column("ipv6", width= 260, anchor=CENTER)
        self.people_records.column("Pass",width= 0, stretch=NO) # be smart
        self.people_records.column("Class", width= 75, anchor=CENTER)
        self.people_records.column("info", width= 50, anchor=CENTER)
        self.people_records.column("idii", width= 75)

        self.people_records.pack(fill =BOTH, expand =1)
        self.people_records.bind("<ButtonRelease-1>", traineeinfo)
        DisplayData()
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = db_verification(root)
    root.mainloop()
        