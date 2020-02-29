import io
import os
import time
import picamera
import threading
import cv2
import PIL
from PIL import Image
from time import sleep

def thread1():
    global camera
    global lock
    while True:
        lock.acquire()
        camera.capture(my_file)
        lock.release()

def thread2():
    global camera
    global lock
    

def main():
    global lock = threading.Lock
    
    os.chdir('/home/pi/Desktop')
    
    my_file = open('my_image.jpg', 'wb')
    stream = io.BytesIO()
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(2)
    
    

#     camera.capture(my_file)
    camera.stop_preview()
    
    stream.seek(0)

    my_file.close()

main()
