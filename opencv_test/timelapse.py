# import os
import io
import os
import time
import picamera
import threading
import cv2
from PIL import Image
from time import sleep

stream = io.BytesIO()
camera = picamera.PiCamera()
# with picamera.PiCamera() as camera:
camera.resolution = (640, 480)
camera.start_preview()
time.sleep(2)
# takePhoto = True
lock = threading.Lock()

def thread_function():
    while True:
        global camera
        global stream
        lock.acquire()
        camera.capture(stream, format='jpeg')
        lock.release()
        stream.seek(0)
        stream.truncate()

def thread_function2():
    global camera
    global stream
    lock.acquire()
    stream.seek(2)
    image = Image.open(stream)

    os.chdir('/home/pi/Desktop')
    # file = "img"
    image.save("img.jpeg")
    # cv2.imwrite('data.jpeg',image)
    # image.show()
    lock.release()

def main():
    
    # os.chdir('/home/pi/Desktop/images')

    # Create the in-memory stream
    x = threading.Thread(target=thread_function)
    y = threading.Thread(target=thread_function2)
    x.start()
    y.start()
    for i in range(10):
        print("new thread started!")
        y = threading.Thread(target=thread_function2)
        y.start()
        y.join()
    
    # "Rewind" the stream to the beginning so we can read its content

main()