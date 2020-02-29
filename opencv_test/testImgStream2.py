import io
import os
import time
import picamera
import threading
import cv2
import PIL
from PIL import Image
from time import sleep
import numpy as np

stream = io.BytesIO()
os.chdir('/home/pi/Desktop/temp')
i = 0
bufEmpty = True
camera = picamera.PiCamera()
camera.resolution = (640, 480)
time.sleep(2)

def streamF():
    global stream
    global camera
    global bufEmpty
    while True:
        camera.capture(stream,format='jpeg')
        bufEmpty = False
        
def showF():
    global stream
    global i
    stream.seek(0)
    
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
    img = cv2.imdecode(data,1)
    cv2.imwrite('test' + str(i) + '.jpg', img)
    cv2.imshow('img', cv2.imread('test' + str(i) + '.jpg'))
    cv2.waitKey(0)    

def main():
    global bufEmpty
    stm = threading.Thread(target=streamF)
    
    stm.start()
    
    while bufEmpty:
        continue

    for i in range(10):
        shw = threading.Thread(target=showF)
        shw.start()
        shw.join()
    
main()
