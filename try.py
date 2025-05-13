import os
import subprocess
import time

#Init Camera=
def CAM_INIT():
#     init_cam = "python C:\prctm_dog\SPOT_cameras\Live_Feed\live_feed\live_feed.py 192.168.80.3 --pixel-format PIXEL_FORMAT_GREYSCALE_U8 -j 100"
#     user = "admin"
#     pswrd = "zmnta28fvcym"
    
# #     os.system(init_cam)
# #     process = os.system(init_cam)
# #     process.stdin.write(user + "\n")
# #     process.stdin.write(pswrd + "\n")
# #     process.stdin.flush()

# # # def auto_log(init_cam, arg=None):
    
    
#     process = os.system(init_cam)
#     process.stdin.write(user + "\n", pswrd + "\n")
#     process.stdin.flush()
#     return process
    init_cam = "python C:/prctm_dog/SPOT_cameras/Live_Feed/live_feed/live_feed.py 192.168.80.3 --pixel-format PIXEL_FORMAT_GREYSCALE_U8 -j 100"
    
    os.system(init_cam)        

CAM_INIT()