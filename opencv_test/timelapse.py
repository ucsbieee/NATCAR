# import os
import io
import time
import picamera
import threading
from PIL import Image
from time import sleep

stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(2)
# takePhoto = True
lock = Lock()

def thread_function():
    while True:
        lock.acquire()
        camera.capture(stream, format='jpeg')
        lock.release()
        stream.seek(0)
        stream.truncate()

def thread_function2():
    lock.acquire()
    stream.seek(2)
    image = Image.open(stream)
    image.show()
    lock.release()

def main():

    # os.chdir('/home/pi/Desktop/images')

    # Create the in-memory stream
    x = threading.Thread(target=thread_function)
    y = threading.Thread(target=thread_function2)
    x.start()
    y.start()
    y.join()

    # "Rewind" the stream to the beginning so we can read its content

main()
