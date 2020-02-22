from picamera import PiCamera
import io
import time
import cv2
import numpy as np

stream = None

def initStream():
    global stream

    stream = io.BytesIO()
    with PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.capture_continuous(stream, 'jpeg', use_video_port=True)

    while True:
        try:
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            image = cv2.imdecode(data, 1)[:, :, ::-1]
            cv2.imshow('Image', image)
        except:
            continue

def closeStream():
    global stream

    if stream is not None:
        stream.close()
        stream = None

def main():
    initStream()

main()
