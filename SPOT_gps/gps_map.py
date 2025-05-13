import tkinter as tk
from tkinter import *
from tkintermapview import TkinterMapView
from flask import Flask, request
import threading
import requests

app = Flask(__name__)
coords = {"lat": 36.016088, "lon": -86.818423}

@app.route('/update', methods=['POST'])
def update_coords():
    if not request.is_json:
        return "Expected JSON data with header 'Content-Type: application/json'", 415

    data = request.get_json(silent=True)

    if data is None:
        return "Invalid JSON body", 400

    try:
        coords["lat"] = float(data.get("lat"))
        coords["lon"] = float(data.get("lon"))
        print(f"Ubicación actualizada: {coords}")
    except Exception as e:
        print(f"ERROR WHEN ACTUALIZING: {e}")
        return "Bad DATA", 400

    return "OK"

def run_flask():
    app.run(host="0.0.0.0", port=6969)      #si no funciona, usar "0.0.0.0"

class MapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("alMOST A real TIME MAP")
        self.root.geometry("300x350+875+425")
        
        root.overrideredirect(True)
        self.root.resizable(width =False, height =False)
        root.attributes("-topmost", True)

        MapFrame = tk.Frame(self.root, width=300, height=350, bd=5, relief=RIDGE, bg="#1f1f1f")
        MapFrame.grid()

        self.map_widget = TkinterMapView(MapFrame, width=290, height=340)
        self.map_widget.pack(fill="both", expand=True)

        self.marker = self.map_widget.set_marker(coords["lat"], coords["lon"], text="SPOT", font =('courier', 8, 'bold'))
        self.map_widget.set_position(coords["lat"], coords["lon"])
        self.map_widget.set_zoom(16)

        self.update_map()

    def update_map(self):
        self.marker.set_position(coords["lat"], coords["lon"])
        self.map_widget.set_position(coords["lat"], coords["lon"])
        self.root.after(3000, self.update_map) 

if __name__ == "__main__":
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    root = tk.Tk()
    app = MapApp(root)
    root.mainloop()

