import PIL.ImageGrab as ImageGrab
import tkinter as tk
from tkinter import Label, Toplevel
from print_ident_color import class_print

from PIL import Image, ImageWin
import win32print
import win32ui

id_vl = 86765

printing_class = "SLAVE 299"
id_print = "86765"
name_print = "IAM"
lastn_print = "IN_JAIL"
class print_class:
    def __init__(self, root):
        root.overrideredirect(True) 
        self.root = root
        
        self.root.geometry("200x75") # width x height + X coordinate + Y coordinate
        self.root.resizable(width =False, height =False)
        root.attributes("-topmost", True)
        
        root.withdraw()
        root.update_idletasks()  # Update "requested size" from geometry manager <--- Hack
        
        #center window/root
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.geometry("+%d+%d" % (x, y))
        
        self.edit_canvas(id_vl, printing_class, id_print, name_print, lastn_print)
    #_________________________________________FUNCTIONS(out of INIT)_________________________________________#
    
    
    def save_as_png(self):
        Label(root, text="PRINTING DATA...").pack()
        self.file = "C:/prctm_dog/canvas.png"
        ImageGrab.grab().crop((713, 168, 1210, 915)).save(self.file)
        
        
    def edit_canvas(self, id_vl, printing_class, id_print, name_print, lastn_print):

        self.id_vl = id_vl
        self.printing_class = printing_class
        self.id_print = id_print
        self.name_print = name_print
        self.lastn_print = lastn_print

        window_canvas = Toplevel(self.root)
        window_canvas.overrideredirect(True)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - 400) // 2
        y = (screen_height - 600) // 2
        window_canvas.geometry("%dx%d+%d+%d" % (400, 600, x, y))

        self.canvitas = class_print(window_canvas)
            
        try:
            self.canvitas.setup_gamer()
            #editar esto para poner las variables
            self.canvitas.info(self.printing_class, self.id_vl, self.name_print, self.lastn_print)
            
        except Exception as e:
            print(f"No se que le pasa :(\n{e}")
            
        root.deiconify() 
        self.root.after(3000, self.save_as_png)
        self.root.after(6000, self.root.withdraw)
        self.root.after(9000, self.print_funct)
        self.root.after(12000, root.destroy)
      
    def print_funct(self):
        
        #printable area
        self.HORZRES= 8
        self.VERTRES= 10
        
        #dots per inch
        self.LOGPIXELSX= 88
        self.LOGPIXELSY= 90
        
        #total area
        self.PHYSICALWIDTH= 110
        self.PHYSICALHEIGHT= 111
    
        #left / top margin
        self.PHYSICALOFFSETX= 112
        self.PHYSICALOFFSETY= 113

        self.printer_name= win32print.GetDefaultPrinter()
        self.file_sjsjs_name= "canvas.png"
        
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(self.printer_name)
        printable_area = hDC.GetDeviceCaps (self.HORZRES), hDC.GetDeviceCaps (self.VERTRES)
        printer_size = hDC.GetDeviceCaps (self.PHYSICALWIDTH), hDC.GetDeviceCaps (self.PHYSICALHEIGHT)
        printer_margins = hDC.GetDeviceCaps (self.PHYSICALOFFSETX), hDC.GetDeviceCaps (self.PHYSICALOFFSETY)

        
        bmp = Image.open (self.file_sjsjs_name)
        
        max_width = 2000  # ancho máximo en la impresora
        max_height = 3000
        image_width, image_height = bmp.size
        scale_x = max_width / image_width
        scale_y = max_height / image_height
        
        if bmp.size[0] > bmp.size[1]:
            bmp = bmp.rotate (90)
        #ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
        scale = min(scale_x, scale_y)#ratios

        # Start the print job
        hDC.StartDoc (self.file_sjsjs_name)
        hDC.StartPage ()

        dib = ImageWin.Dib (bmp)
        scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
        x1 = int ((printer_size[0] - scaled_width) / 2)
        y1 = int ((printer_size[1] - scaled_height) / 2)
        x2 = x1 + scaled_width
        y2 = y1 + scaled_height
        dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

        hDC.EndPage ()
        hDC.EndDoc ()
        hDC.DeleteDC ()

            
if __name__ == "__main__":
    root = tk.Tk()
    application = print_class(root)
    root.mainloop()


