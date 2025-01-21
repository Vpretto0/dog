
from tkinter import ttk
from tkinter import *
import tkinter.messagebox

import pymysql
import db_identity
from db_identity import *

import io
from io import BytesIO
from PIL import Image


    
class photo_class:
    print("photo.py is working")
    def __init__(self, root):
        
        root.overrideredirect(True)
        style = ttk.Style()
        style.theme_use('clam')
        
        
        root.configure(bg='#f1f1f1')
        self.root = root
        titlespace = " "
        self.root.title(102 * titlespace + "Photo Frame")
        self.root.geometry("235x380+1080+380") # width x height + X coordinate + Y coordinate
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
        
        
        def get_image():

            try:
                print("Starting SEARCH function")
                conn, c  = db_identity.create_connection()
                    
                try: 
                               
                    fotito="SELECT photo FROM people WHERE id = '%s' "
                    
                    #conn.commit()
                    c.execute(fotito)
                    data_display=c.fetchall() 

                    if data_display is not None:
                        
                        data= io.BytesIO(data_display[0][0])
                            #get first image from db and convert it to bytes   
                        imagen=Image.open(data)                   
                        imagen.show()
                        print("show_image function working")
                        
                    else:
                        tkinter.messagebox.showinfo("Error", "no data ")
                        
                        
                except Exception as e:
                    print(F"Error -> {e}")
                    
                finally:
                    db_identity.close_connection(conn, c)
                    #image.save('image.png')    
                        

            except Exception as e:
                tkinter.messagebox.showinfo("Error", f"It's not working: {e}")
                

            def display_image():
                pass
            
        
        #_______________________________________________________________________________________________________#
        
        self.btnChange = Button(BottomFrame, text = "Change", font =('courier', 10, 'bold'), fg='white', bg = '#212121', activebackground='gray', command = show_image,
            padx =5, pady=1, width =8, height =1,  bd =5). grid(row =0, column =0, padx =3)
        
        self.btnDelete = Button(BottomFrame, text = "DELETE", font =('courier', 10, 'bold'), fg = "red", bg = '#212121', activebackground='red',
            padx =5, pady=1, width =8, height =1, bd =5). grid(row =0, column =1, padx =3)
        #_______________________________________________________________________________________________________#
        
        
if __name__=='__main__':
    root = Tk()
    aplication = photo_class(root)
    root.mainloop()