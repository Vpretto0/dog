from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox

import db_identity

import io
from PIL import Image, ImageTk


import barcode
from barcode.writer import ImageWriter


def generate_barcode(alphanum_string):
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

    #cambiar
    return barcode_instance.save("barcode", options=module) #chage for barcode_png on the database
