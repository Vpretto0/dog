import cv2
import socket
import pickle
import numpy as np

socketsito = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = "192.168.80.3"   
port = 6666
socketsito.bind((ip, port))

while True:
    x = socketsito.recvfrom(1000000)
    clientip = x[1][0]
    data = x[0]
    
    data = pickle.loads(data)
    
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cv2.imshow("Img Server", img)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break
    
cv2.destroyAllWindows()
    
