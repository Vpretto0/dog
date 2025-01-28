#CANVA
from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()
root.geometry('450x650')
root.title('Canva')

canvas = tk.Canvas(root, width=400, height=600, bg='white')
canvas.pack(anchor=tk.CENTER, expand=True)


#___________________________________________________BACKGROUND________________________________________________#
canvas.create_rectangle(4,4,399,599, fill= '#003da6', width=0)

#___________________________________________________LOGO______________________________________________________#
canvas.create_rectangle(346,60,390,106, fill= 'white', width=0)

points = ((346, 106),(346, 115), (368, 106),)
canvas.create_polygon(*points, fill='white')
points = ((390, 106),(390, 115), (368, 106),)
canvas.create_polygon(*points, fill='white')


image_logo= tk.PhotoImage(file="C:/prctm_dog/images/BHS(44px).png")
canvas.create_image((346, 63), image=image_logo, anchor='nw')

#___________________________________________________TITLE_____________________________________________________#
canvas.create_rectangle(4,4,399,60, fill= 'black', width=0)
canvas.create_text(200, 35, text='BRENTWOOD HIGH', font=('Arial', 20), fill='white')
#___________________________________________________PHOTO_____________________________________________________#
#canvas.create_rectangle(4,425,399,599, fill= 'black', width=0)
#no preguntes como
main_photo = Image.open("C:/prctm_dog/photo.png")
resized_photo = main_photo.resize((132, 178))
image_photo = ImageTk.PhotoImage(resized_photo)

canvas.create_image((25, 80), image=image_photo, anchor='nw')

#___________________________________________________INFO FRAME________________________________________________#
frame_photo = Image.open("C:/prctm_dog/images/boring_text.png")
resized_frame = frame_photo.resize((400, 75))
frame_photo = ImageTk.PhotoImage(resized_frame)

canvas.create_image((2, 350), image=frame_photo, anchor='nw')

#___________________________________________________BARCODE___________________________________________________#
canvas.create_rectangle(4,425,399,599, fill= 'black', width=0)

image_barcode = tk.PhotoImage(file="C:/prctm_dog/barcode.png")
canvas.create_image((50, 455), image=image_barcode, anchor='nw')

#___________________________________________________FRAME_____________________________________________________#
def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
        
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)

#___________________________________________________INFO______________________________________________________#
def info(class_print, id_print, name_print, lastn_print):
    canvas.create_text(265, 200, text=f"{class_print} of \nBrentwood High \nSchool", font=('verdana', 15, 'bold'), fill='white', justify='left')
    canvas.create_text(231, 100, text=f"{id_print}", font=('verdana', 16, 'bold'), fill='white', justify='center')
    canvas.create_text(200, 305, text=f"{name_print} {lastn_print}", font=('verdana', 17, 'bold'), fill='white')
    
info("Student", "0001", "John", "Doe")




canvas.create_rectangle(4, 4, 399, 599, width=3, outline='white', fill='')
round_rectangle(5, 5, 399, 599, radius=20, width=2, outline='black', fill='')

root.mainloop()