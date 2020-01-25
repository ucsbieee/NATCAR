import RPICommReal
import sys
import serial
from lineFollowRPI import lineFollow
sys.path.insert(1, '../pi_cam')
from timelapseReal import takePicture

s = serial.Serial('/dev/ttyACM0', 9600)
takePicture(0)
a, shift = lineFollow(0)
s.write(str.encode(chr(a)))
RPICommReal.comm(chr(a))