from termios import tcflush, TCIFLUSH
import serial
import time
import sys
import testclass

def getSignedNumber(number, bitLength):
                mask = pow(2,bitLength) - 1
                if number & (1 << (bitLength - 1)):
                        return number | ~mask
                else:
                        return number & mask

def bytes2val(highbyte, lowbyte):
                number = (highbyte<<8)+lowbyte
                return getSignedNumber(number,16)

# main
#ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)
robot = testclass.Roomba()
robot.ser.flushInput()
robot.ser.flushOutput()
robot._start()
robot._safe()
robot._clean()
#robot._direct()
time.sleep(2)
#robot._stream()
for i in range(1,5):
	time.sleep(2)
	robot._sensors()
	#tcflush(sys.stdin, TCIFLUSH)
        #resp=ser.read(9)
        #time.sleep(0.3)
	#print('distance')
        #print (bytes2val(ord(resp[3]),ord(resp[4])))
	#print('angle')
        #print (bytes2val(ord(resp[6]),ord(resp[7])))
time.sleep(2)
robot._safe()
