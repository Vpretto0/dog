import cv2
import socket
import pickle
import os
import numpy as np

size_x = 60
class Camera_4:
    
    def __init__(self, size_x):
        
        self.size_x = size_x
        
        socketsito = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socketsito.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

        server_ip = "192.168.80.3"  #si da problemas improvisar
        server_port = 6666

        cap = cv2.VideoCapture(3)
        cap.set(3, 1280)  #width
        cap.set(4, 720)  #height 

        def rescale_frame(img, percent=size_x):
            width = int(img.shape[1] * percent/ 100)
            height = int(img.shape[0] * percent/ 100)
            dim = (width, height)
            return cv2.resize(img, dim, interpolation =cv2.INTER_AREA)


        while cap.isOpened():
            ret, img = cap.read()
            framesize = rescale_frame(img, percent=size_x)
            cv2.imshow('', framesize)
            
            ret, buffer = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
            x_as_bytes = pickle.dumps(buffer)
            socketsito.sendto((x_as_bytes), (server_ip, server_port))
            
            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        cv2.destroyAllWindows()
        cap.release()   
    
if __name__ == "__main__":
    application = Camera_4(size_x)
    

