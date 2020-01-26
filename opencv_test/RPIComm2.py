import serial
import time
import sys
from lineFollow2 import lineFollow
sys.path.insert(1, '../pi_cam')
from timelapse2 import takePicture

def comm(firstAngle):
    s = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(1.65)
    try:
        firstAngle = ord(firstAngle)
        firstAngle = firstAngle/3.6
        firstAngle = 25-firstAngle
        firstAngle = firstAngle + 90
        firstAngle = int(firstAngle)
        s.write(str.encode(chr(firstAngle)))
        i = 1
        while True:
            response = s.readline()
            print(response)
            if response == b'DONE\r\n':
                takePicture(i)
                angle, shift = lineFollow(i)
                #time.sleep(0.2)
                angle = angle/3.6
                angle = 25-angle
                angle = angle + 90
                angle = int(angle)
                s.write(str.encode(chr(angle)))
                i+=1
    except KeyboardInterrupt:
        s.close()
    
# if __name__ == '__main__':
#     angle = '1'
#     comm(angle)             