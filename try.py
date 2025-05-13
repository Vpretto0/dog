import os
import subprocess
import time
from tkinter import messagebox


user = "admin"
pswrd = "zmnta28fvcym"
init_cam = "python SPOT_cameras/live_feed_controls.py 192.168.80.3 --pixel-format PIXEL_FORMAT_GREYSCALE_U8 -j 100"
init_map = "python SPOT_gps/gps_listener.py 192.168.80.3"
init_wasd = "python SPOT_wasd/wasd.py 192.168.80.3"
init_estop = "python SPOT_estop/estop.py 192.168.80.3"

def start_with_the_password(init_cam, user, pswrd):
    args = init_cam.split()
    process = subprocess.Popen(     #POPEN
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    process.stdin.write(user + "\n")
    process.stdin.write(pswrd + "\n")
    process.stdin.flush()
    return process  #no alvidar return

def pwll(command):
    pwll_command = f'powershell -NoExit -Command "{command}"'
    subprocess.Popen(["powershell", "-NoExit", "-Command", command])
    
def start(command, user, pswrd):
        try:
            start_with_the_password(command, user, pswrd)
        except Exception as e:
            print(f"Error al  MI script {command}: {e}")
            return None
            
def wasd_button():
    messagebox.showinfo("Manual Mode", "Controls: \nW = Forward\nS = Backward\nA = Left\nD - Right\nQ = Turn Left\nE = Turn Right                           ")
    messagebox.showinfo("Manual Mode", "Commands: \nTAB = Quit\nT = Time-sync\nSPACE = Estop\nP = Power\nI = Take Image\nO = Video mode\nf = Stand\nr = Self-right\nv = Sit\nb = Battery-change\nESC = Stop\n1 = Return/Acquire Lease                   ")
    start(init_wasd, user, pswrd)


#   [ ]     COMO ABRIRLO CON UNA TERMINAL
#   [ ]     


pwll(wasd_button())