from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import RPIComm2
import sys
import serial
from lineFollow2 import lineFollow
sys.path.insert(1, '../pi_cam')
from timelapse2 import takePicture

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = (PiRGBArray(camera, size=(640, 480)))
#s = serial.Serial('/dev/ttyACM0', 9600)
# takePicture(0)
# 
# a, shift = lineFollow(0)
# if a is None:
#     a = 90
# a = a/3.6
# a = 25-a
# a = a + 90
# a = int(a)
# s.write(str.encode(chr(a)))
RPIComm2.comm(chr(90))
