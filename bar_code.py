
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox

import db_identity

import io
from PIL import Image, ImageTk

id_vl= 86765   
   
class barcode_class:
    print("bar_code.py is working")
    def __init__(self, root, id_vl):
        
        root.overrideredirect(True)
        style = ttk.Style()
        style.theme_use('clam')
        
        root.configure(bg='#f1f1f1')
        self.root = root 
        self.id_vl = id_vl
        titlespace = " "
        self.root.title(102 * titlespace + "Barcode")
        self.root.geometry("420x205+950+520") # width x height + X coordinate + Y coordinate
        self.root.resizable(width =False, height =False)
        self.root.configure(bg = '#1f1f1f')
        
        MainFrame = Frame(self.root, bd =10, width =500, height =200, relief = RIDGE, bg = '#1f1f1f')
        MainFrame.grid()
        
        TitleFrame = Frame(MainFrame, bd =7, width =400, height =45, relief = RIDGE, bg = '#1f1f1f')
        TitleFrame.grid(row =0, column =0)
        
        BarFrame = Frame(MainFrame, bd =5, width =400, height =130, relief = RIDGE, bg = '#1f1f1f')
        BarFrame.grid(row =1, column =0)
        
        LeftFrame = Frame(TitleFrame, bd =7, width =40, height=40, bg = 'green')#put print func and icon here
        LeftFrame.grid(row =0, column =1)
        
        # TopFrame = Frame(TopFrame3, bd =5, width =300, height =228,padx =2, pady =4, bg = '#1f1f1f')
        # TopFrame.pack(side =TOP, padx =0, pady =0)
        # BottomFrame = Frame(TopFrame3, bd =7, width =45, height =45,padx =2, pady =4, bg = '#1f1f1f')
        # BottomFrame.pack(side =BOTTOM, padx =0, pady =0)
        # #_______________________________________________________________________________________________________#
        
        self.lbltitle = Label(TitleFrame, font =('courier', 16, 'bold'),text ="BARCODE", bd =5, fg='white', bg='#1f1f1f')
        self.lbltitle.grid(row =0, column =0, padx =121)
        #_______________________________________________________________________________________________________#
        
            #182x228y
        code = Frame(BarFrame, width =400, height =125, bg = '#1f1f1f') 
        code.pack()
        #photo frame
        
        canvas = tkinter.Canvas(code, background = 'black', width=385, height=120) # problema si introduces directamente esto: image= frame_image
        canvas.grid(sticky = 'nsew')
        #_______________________________________________________________________________________________________#
        
        
        def image_barcode():
            try:
                print("Starting IMAGE_BARCODE function")
                conn, c  = db_identity.create_connection()
                    
                try: 
                    codebar="SELECT barcode FROM people WHERE id = %s"
                    c.execute(codebar, (id_vl,))
                    data_display=c.fetchall() 
                    try:
                    
                        data= io.BytesIO(data_display[0][0])                   
                        print("show_image function is working")
            
                        load_image(data)
                        canvas.create_image(0, 0, anchor="nw", image=frame_code)
                        canvas.image = frame_code 
                            
                    except Exception:
                        tkinter.messagebox.showinfo("Backend is Sad :(", """   no image data found""")
                        
                except Exception as e:
                    print(F"Error -> {e}")
                    
                finally:
                    db_identity.close_connection(conn, c)
                    #image.save('image.png')    

            except Exception as e:
                print(f"Error -> {e}")
                
        def load_image(data):
                global frame_code
                    
                bar_imagen=Image.open(data) 
                bar_imagen= bar_imagen.resize((385, 120))
                frame_code= ImageTk.PhotoImage(bar_imagen)
                    
        image_barcode()
        
        #_______________________________________________________________________________________________________#
        
        # self.btnChange = Button(BottomFrame, text = "Change", font =('courier', 10, 'bold'), fg='white', bg = '#212121', activebackground='gray',
        #     padx =5, pady=1, width =8, height =1,  bd =5). grid(row =0, column =0, padx =3)
        
        # self.btnDelete = Button(BottomFrame, text = "DELETE", font =('courier', 10, 'bold'), fg = "red", bg = '#212121', activebackground='red',
        #     padx =5, pady=1, width =8, height =1, bd =5). grid(row =0, column =1, padx =3)
        #_______________________________________________________________________________________________________#
        
        
        #canva
        #_______________________________________________________________________________________________________#
        
        
if __name__=='__main__':
    root = Tk()
    aplication = barcode_class(root, id_vl) 
    #aplication.get_Image()
    
    root.mainloop()