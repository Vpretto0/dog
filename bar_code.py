
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox

import db_identity

import io
from PIL import Image, ImageTk

import barcode
from barcode.writer import ImageWriter

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
        
        root.attributes("-topmost", True)
        
        MainFrame = Frame(self.root, bd =10, width =500, height =200, relief = RIDGE, bg = '#1f1f1f')
        MainFrame.grid()
        
        TitleFrame = Frame(MainFrame, bd =7, width =400, height =45, relief = RIDGE, bg = '#1f1f1f')
        TitleFrame.grid(row =0, column =0)
        
        BarFrame = Frame(MainFrame, bd =5, width =400, height =130, relief = RIDGE, bg = '#1f1f1f')
        BarFrame.grid(row =1, column =0)
        
        LeftFrame = Frame(TitleFrame, width =40, height=40, bg = '#1f1f1f')#put print func and icon here
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
        def generate_barcode(alphanum_string):
            print("HELLO! from bar_generator.py")
            module = {
                'module_width': 0.3,
                'module_height': 7.0,
                'quiet_zone': 1.0,
                'font_size': 0,
                'text_distance': 0.0,
                'background': 'white',
                'foreground': 'black',
                'write_text': False
            }

            code128 = barcode.get_barcode_class('code128') # The Code128 is a barcode symbology.
            barcode_instance = code128(alphanum_string, writer=ImageWriter())

            
            return barcode_instance.save("barcode", options=module)
              
        #AJUSTAR RUTA DE GUARDADO
        def pathfile():
            global filepath
            filepath = "C:/prctm_dog/barcode.png"
                
            new_image = Image.open(filepath)
            width, height = int(385), int(120)
            new_image = new_image.resize((width, height))
            
            
        def barcode_id():
            try:
                print("Starting SAVE(barcode version) function")
                conn, c  = db_identity.create_connection()
                    
                try:
                    pathfile()
                    generate_barcode(str(id_vl))
                    with open(filepath, 'rb') as file: # <"read binary">
                        bar = file.read()
                            
                    sql = "UPDATE people SET barcode= %s WHERE id = %s "
                    c.execute(sql, (bar, id_vl))
                    conn.commit()
                    print("IT'S WORKING!!")
                        
                except Exception as e:
                    print(F"Error -> {e}")
                    
                finally:
                    db_identity.close_connection(conn, c)
                        
            except Exception as e:
                tkinter.messagebox.showinfo("Error", f"It's not working: {e}")
        
        #_______________________________________________________________________________________________________#
        self.image_path= PhotoImage(file="C:/prctm_dog/images/printer-24.png") 
        self.btnChange= Button(LeftFrame,text= "click", image=self.image_path, bg= '#1f1f1f', fg= 'green', borderwidth=0, cursor='hand2', command=barcode_id). pack(side =LEFT, padx =6)

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