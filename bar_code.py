from tkinter import *
from tkinter import ttk
import tkinter.messagebox

import io
from PIL import Image, ImageTk

import db_identity

import barcode
from barcode.writer import ImageWriter

from click_here import print_class


id_vl = 86765
state_action = False

printing_class = "prisioner"
id_print = "69696969"
name_print = "i am"
lastn_print = "in jail"
   
class barcode_class:
    print("bar_code.py is working")
    def __init__(self, root, id_vl, state_action, printing_class, id_print, name_print, lastn_print):
        
        root.overrideredirect(True)
        style = ttk.Style()
        style.theme_use('clam')
        
        root.configure(bg='#f1f1f1')
        
        self.root = root 
        self.id_vl = id_vl

        self.printing_class = printing_class
        self.id_print = id_print
        self.name_print = name_print
        self.lastn_print = lastn_print
    
        self.state_action = state_action #si
        
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
        #_______________________________________________________________________________________________________#
        
        self.lbltitle = Label(TitleFrame, font =('courier', 16, 'bold'),text ="BARCODE", bd =5, fg='white', bg='#1f1f1f')
        self.lbltitle.grid(row =0, column =0, padx =121)
        #_______________________________________________________________________________________________________#
            #182x228y
        code = Frame(BarFrame, width =400, height =125, bg = '#1f1f1f') 
        code.grid(row =0, column =0)
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
                        tkinter.messagebox.showinfo("Backend is Sad :(", """   no barcode data found""")
                        
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
            print("si no ves esto, no se guardo la imagen")
            

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
                
        def action_state(state_action):
            if state_action == True:
                barcode_id()
                state_action = False
            else:
                print("Barcode is already generated")
                return    
        #_______________________________________________________________________________________________________#
        
        def print_canvass():
            id_vl_ii = self.id_vl
            printing_class_ii = self.printing_class
            id_print_ii = self.id_print
            name_print_ii = self.name_print
            lastn_print_ii = self.lastn_print
            
            click_here_window = Toplevel(self.root)
            click_here_window.overrideredirect(True)
            canva_screen = print_class(click_here_window)
            canva_screen.edit_canvas(id_vl_ii, printing_class_ii, id_print_ii, name_print_ii, lastn_print_ii)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            x = (screen_width - 400) // 2
            y = (screen_height - 600) // 2
            click_here_window.geometry("%dx%d+%d+%d" % (400, 600, x, y))

            self.imprimiendo = print_class(click_here_window)
        #_______________________________________________________________________________________________________#
        
        self.image_path= PhotoImage(file="C:/prctm_dog/images/printer-24.png") 
        self.btnChange= Button(LeftFrame,text= "click", image=self.image_path, bg= '#1f1f1f', fg= 'green', borderwidth=0, command= print_canvass, cursor='hand2').grid(row=0, column=0, padx=6, pady=6)
        #_______________________________________________________________________________________________________#
        
        image_barcode()
        action_state(state_action)
        #_______________________________________________________________________________________________________#
     
if __name__=='__main__':
    root = Tk()
    #para obtener la info y editar el canvas para imprimir (por si no me acuerdo)
    aplication = barcode_class(root, id_vl, state_action, printing_class, id_print, name_print, lastn_print)
    #aplication.get_Image()
    root.mainloop()

    