from time import sleep
import picamera
import cv2

camera = picamera.PiCamera()

camera.resolution = (640, 480);
sleep(2)
camera.capture('/home/pi/Desktop/inputimg/testimg6.jpg')
#img = cv2.imread('/home/pi/Desktop/testimg3.jpg')

camera.close()
