import serial
import time

def comm(angle):
    s = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(1.65)
    try:
        angleInt = ord(angle);
        s.write(str.encode(angle))
        while True:
            response = s.readline()
            print(response)
#             if response == b'DONE\r\n' and angleInt > 60:
#                 print("test")
                #angleInt-=1
            s.write(str.encode(chr(angleInt)))
            angleInt-=1
    except KeyboardInterrupt:
        s.close()
    
#if __name__ == '__main__':
#    comm(angle)               