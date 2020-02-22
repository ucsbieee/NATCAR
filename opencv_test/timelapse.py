# import os
import io
import time
import picamera
from PIL import Image
from time import sleep

# takePhoto = True

def main():

    # os.chdir('/home/pi/Desktop/images')

    # Create the in-memory stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        time.sleep(2)
        camera.capture(stream, format='jpeg')
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(2)
    image = Image.open(stream)
    image.show()

main()