import cv2
import socket
import pickle
import os
import numpy as np

socketsito = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketsito.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

server_ip = "192.168.80.3" #cambiar a la ip si da problemas
server_port = 6666

cap = cv2.VideoCapture(1)   #Esto se puede cambiar 
cap.set(3, 640)  #width
cap.set(4, 480)  #height 

while cap.isOpened():
    ret, img = cap.read()
    
    cv2.imshow("Img Client", img)
    
    ret, buffer = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    x_as_bytes = pickle.dumps(buffer)
    socketsito.sendto((x_as_bytes), (server_ip, server_port))
    
    if cv2.waitKey(2) & 0xFF == 27:
        break
    
cv2.destroyAllWindows()
cap.release()   
    
    

