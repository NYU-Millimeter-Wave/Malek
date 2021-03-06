from termios import tcflush, TCIFLUSH
import time
import math
import serial
import sys
# some module-level definitions for the robot commands
START = chr(128)    # already converted to bytes...
BAUD = chr(129)     # + 1 byte
CONTROL = chr(130)  # deprecated for Create
SAFE = chr(131)
FULL = chr(132)
POWER = chr(133)
SPOT = chr(134)     # Same for the Roomba and Create
CLEAN = chr(135)    # Clean button - Roomba
COVER = chr(135)    # Cover demo - Create
MAX = chr(136)      # Roomba
DEMO = chr(136)     # Create
DRIVE = chr(137)    # + 4 bytes
MOTORS = chr(138)   # + 1 byte
LEDS = chr(139)     # + 3 bytes
SONG = chr(140)     # + 2N+2 bytes, where N is the number of notes
PLAY = chr(141)     # + 1 byte
SENSORS = chr(142)  # + 1 byte
FORCESEEKINGDOCK = chr(143)  # same on Roomba and Create
# the above command is called "Cover and Dock" on the Create
DRIVEDIRECT = chr(145)       # Create only
STREAM=chr(148)
#STREAM_DIS_ANG = [chr(148), chr(2) ,chr(19), chr (20)]       # Create only
QUERYLIST = chr(149)       # Create only
PAUSERESUME = chr (150)
#PAUSE = chr(150 0)       # Create only
#RESUME= chr(150 1)
#### Sean

SCRIPT = chr(152)
ENDSCRIPT = chr(153)
WAITDIST = chr(156)
WAITANGLE = chr(157)

# the four SCI modes
# the code will try to keep track of which mode the system is in,
# but this might not be 100% trivial...
OFF_MODE = 0
PASSIVE_MODE = 1
SAFE_MODE = 2
FULL_MODE = 3

# the sensors
BUMPS_AND_WHEEL_DROPS = 7
WALL_IR_SENSOR = 8
CLIFF_LEFT = 9
CLIFF_FRONT_LEFT = 10
CLIFF_FRONT_RIGHT = 11
CLIFF_RIGHT = 12
VIRTUAL_WALL = 13
LSD_AND_OVERCURRENTS = 14
DIRT_DETECTED = 15
INFRARED_BYTE = 17
BUTTONS = 18
DISTANCE = chr(19)
ANGLE = chr(20)
CHARGING_STATE = 21
VOLTAGE = 22
CURRENT = 23
BATTERY_TEMP = 24
BATTERY_CHARGE = 25
BATTERY_CAPACITY = 26
WALL_SIGNAL = 27
CLIFF_LEFT_SIGNAL = 28
CLIFF_FRONT_LEFT_SIGNAL = 29
CLIFF_FRONT_RIGHT_SIGNAL = 30
CLIFF_RIGHT_SIGNAL = 31
CARGO_BAY_DIGITAL_INPUTS = 32
CARGO_BAY_ANALOG_SIGNAL = 33
CHARGING_SOURCES_AVAILABLE = 34
OI_MODE = 35
SONG_NUMBER = 36
SONG_PLAYING = 37
NUM_STREAM_PACKETS = 38
REQUESTED_VELOCITY = 39
REQUESTED_RADIUS = 40
REQUESTED_RIGHT_VELOCITY = 41
REQUESTED_LEFT_VELOCITY = 42
ENCODER_LEFT = 43
ENCODER_RIGHT = 44
LIGHTBUMP = 45
LIGHTBUMP_LEFT = 46
LIGHTBUMP_FRONT_LEFT = 47
LIGHTBUMP_CENTER_LEFT = 48
LIGHTBUMP_CENTER_RIGHT = 49
LIGHTBUMP_FRONT_RIGHT = 50
LIGHTBUMP_RIGHT = 51

# others just for easy access to particular parts of the data
POSE = 100
LEFT_BUMP = 101
RIGHT_BUMP = 102
LEFT_WHEEL_DROP = 103
RIGHT_WHEEL_DROP = 104
CENTER_WHEEL_DROP = 105
LEFT_WHEEL_OVERCURRENT = 106
RIGHT_WHEEL_OVERCURRENT = 107
ADVANCE_BUTTON = 108
PLAY_BUTTON = 109

#                    0 1 2 3 4 5 6 7 8 9101112131415161718192021222324252627282930313233343536373839404142434445464748495051
SENSOR_DATA_WIDTH = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,2,2,1,2,2,2,2,2,2,2,1,2,1,1,1,1,1,2,2,2,2,2,2,1,2,2,2,2,2,2]

#The original value was 258.0 but my roomba has 235.0
WHEEL_SPAN = 235.0
WHEEL_DIAMETER = 72.0
TICK_PER_REVOLUTION = 508.8 # original 508.8
TICK_PER_MM = TICK_PER_REVOLUTION/(math.pi*WHEEL_DIAMETER)

# on my floor, a full turn is measured as sth like 450 deg
# add an error to the computation to account for that.
ANGULAR_ERROR = 360.0/450.0

class Roomba:
	ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)
        def _write(self,byte):
            self.ser.write(byte)
        
        def _start(self):
                self._write( START )
                # they recommend 20 ms between mode-changing commands
                time.sleep(0.25)
                # change the mode we think we're in...
    		return
        
        def _safe(self):
   		self._write( SAFE )
         	time.sleep(0.25)
        	return
        
        def _clean(self):
        	self._write( CLEAN )
        	time.sleep(0.25)
       		return
 
        def getSignedNumber(self,number, bitLength):
                mask = pow(2,bitLength) - 1
                if number & (1 << (bitLength - 1)):
                        return number | ~mask
                else:
                        return number & mask

        def bytes2val(self,highbyte, lowbyte):
                number = (highbyte<<8)+lowbyte
                return self.getSignedNumber(number,16)

        '''def _stream(self):
        	self._write( STREAM )
        	self._write( chr(2) )
        	self._write( DISTANCE )
        	self._write( ANGLE )
		#time.sleep(0.5)
		for i in range(1,200):
			#time.sleep(3)
			self.ser.flushInput()
			self.ser.flushOutput()
			resp=self.ser.read(9)
			print('distance')
        		print (self.bytes2val(ord(resp[3]),ord(resp[4])))
        		print('angle')
        		print (self.bytes2val(ord(resp[6]),ord(resp[7])))
			tcflush(sys.stdin, TCIFLUSH)
		time.sleep(2)
	    	return'''

	def _sensors(self):
		self._write( SENSORS )
                self._write( DISTANCE )
		resp=self.ser.readline()
		print ('dans le tableau distance, on a')
		print (int((resp).encode('hex'), 16))
		self._write( SENSORS )
                self._write( ANGLE )
		print('dans le tableau angle, on a')
		resp1=self.ser.readline()
		print (int((resp1).encode('hex'), 16))
		print ('avec highbyte, lowbyte,on obtient distance')
		print (self.bytes2val(ord(resp[0]),ord(resp[1])))
		print ('avec highbyete,angle')
		print (self.bytes2val(ord(resp1[0]),ord(resp1[1])))
		return

        def _pausestream(self):
        	self._write( PAUSERESUME )
        	self._write(chr(0))
        	return

        def _resumestream(self):
        	self._write( PAUSERESUME )
            	self._write(chr(1))
	    	return

	def _direct(self):
		self._write ( DRIVEDIRECT )
		time.sleep(0.25)
		return
