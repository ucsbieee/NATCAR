import RPIComm
import sys
import serial
from lineFollow import lineFollow
sys.path.insert(1, '../pi_cam')
from timelapse import takePicture

s = serial.Serial('/dev/ttyACM0', 9600)
takePicture(i)
a, s = lineFollow(i)
s.write(str.encode(chr(a)))
RPIComm.comm(chr(a))