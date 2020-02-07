import smbus
from time import sleep
import csv

from datetime import datetime
import math

from digital_acquisition import read_current
from plot import plotFromFile
#import keyboard


import sys
arg=sys.argv[1]

_SECONDS_=int(sys.argv[2])
_PATH_FILE_="data/test_"+arg+".csv.txt"
_PLOT_ENABLED_=True
_DEBUG_ENABLED_=True




# Set the Hotkeys to get the event from the Keyboard
global event
event = "Still"
'''
def setM(ev):
    global event
    event = "Moving"
keyboard.on_press_key("m", setM)

def setS(ev):
    global event
    event = "Still"
keyboard.on_press_key("s", setS)

def setC(ev):
    global event
    event = "Crash"
keyboard.on_press_key("c", setC)

def setT(ev):
    global event
    event = "Tap"
keyboard.on_press_key("t", setT)
'''

# select the correct i2c bus for this revision of Raspberry Pi
revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8] == "Revision"]+['0000'])[0]
bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0)

# ADXL345 constants
EARTH_GRAVITY_MS2 = 9.80665
SCALE_MULTIPLIER = 0.004

DATA_FORMAT = 0x31
BW_RATE = 0x2C
POWER_CTL = 0x2D

BW_RATE_1600HZ = 0x0F
BW_RATE_800HZ = 0x0E
BW_RATE_400HZ = 0x0D
BW_RATE_200HZ = 0x0C
BW_RATE_100HZ = 0x0B
BW_RATE_50HZ = 0x0A
BW_RATE_25HZ = 0x09

RANGE_2G = 0x00
RANGE_4G = 0x01
RANGE_8G = 0x02
RANGE_16G = 0x03

MEASURE = 0x08
AXES_DATA = 0x32


class ADXL345:

    address = None

    def __init__(self, address=0x53):
        self.address = address
        self.setBandwidthRate(BW_RATE_25HZ)
        self.setRange(RANGE_4G)
        self.enableMeasurement()

    def enableMeasurement(self):
        bus.write_byte_data(self.address, POWER_CTL, MEASURE)

    def setBandwidthRate(self, rate_flag):
        bus.write_byte_data(self.address, BW_RATE, rate_flag)

    # set the measurement range for 10-bit readings
    def setRange(self, range_flag):
        value = bus.read_byte_data(self.address, DATA_FORMAT)

        value &= ~0x0F
        value |= range_flag
        value |= 0x08

        bus.write_byte_data(self.address, DATA_FORMAT, value)

    # returns the current reading from the sensor for each axis
    #
    # parameter gforce:
    #    False (default): result is returned in m/s^2
    #    True           : result is returned in gs
    def getAxes(self, gforce=False):
        bytes = bus.read_i2c_block_data(self.address, AXES_DATA, 6)

        x = bytes[0] | (bytes[1] << 8)
        if(x & (1 << 16 - 1)):
            x = x - (1 << 16)

        y = bytes[2] | (bytes[3] << 8)
        if(y & (1 << 16 - 1)):
            y = y - (1 << 16)

        z = bytes[4] | (bytes[5] << 8)
        if(z & (1 << 16 - 1)):
            z = z - (1 << 16)

        x = x * SCALE_MULTIPLIER
        y = y * SCALE_MULTIPLIER
        z = z * SCALE_MULTIPLIER

        if gforce == False:
            x = x * EARTH_GRAVITY_MS2
            y = y * EARTH_GRAVITY_MS2
            z = z * EARTH_GRAVITY_MS2

        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)

        return {"x": x, "y": y, "z": z}

#TODO:: If while(true) is used, after a while it crash
if __name__ == "__main__":
    # if run directly we'll just create an instance of the class and output the current readings
    adxl345 = ADXL345()
    # Try to catch the Interrupt and close the file saving the results 
    try:
        # Interval to update measures
        timeInterval = 0.05
        # Dictionary used to store the information of the measures
        values = dict(x=0, y=0, z=0, norm=0, current=0, roll=0, pitch=0, time=0, event='Still')

        # Open File and write the head
        f = open(_PATH_FILE_, "w+")
        writer = csv.writer(f)
        writer.writerow(values.keys())
        
        # Loop 
        i = 0
        seconds = _SECONDS_
        while(i < seconds/timeInterval):
            # Save the time of the measurement
            values["time"] = datetime.now()
            # Get the values of the axis from the accellerometer
            axes = adxl345.getAxes(True)
            values['x'] = axes['x']
            values['y'] = axes['y']
            values['z'] = axes['z']
            # Get the current value from the current sensor
            current=read_current()
            values['current']=current
            # Compute additional information using the axes values
            values['norm'] = math.sqrt((values['x'] * values['x']) + (values['y'] * values['y']) + (values['z'] * values['z']))
            values['roll'] = math.atan2(values['y'], values['z']) * 180 / math.pi
            values['pitch'] = math.atan2(-1*values['x'], math.sqrt(values['y']*values['y']+values['z']*values['z'])) * 180 / math.pi
            # Get the value of the event using the keyboard hotkeys
            values['event'] = event
            # Save the information on the file
            writer.writerow(values.values())
            # Print the result for Debug
            if(_DEBUG_ENABLED_):
                print(str(i) + " ADXL345 on address 0x%x:" % (adxl345.address))
                print("   x = %.3fG" % (values['x']))
                print("   y = %.3fG" % (values['y']))
                print("   z = %.3fG" % (values['z']))
                print("   roll = %f" % (values['roll']))
                print("   pitch = %f" % (values['pitch']))
                print("   event = %s" % (values["event"]))
                print("   norm = %s" % (values["norm"]))
                print("   current = %s" % (values["current"]))
            # Wait for the designed interval
            sleep(timeInterval)
            # Update the index
            i += 1
    # In case of a sudden interrupt, print the cause
    except KeyboardInterrupt as k:
        print("Keyboard: " + str(k))
    except Exception as e:
        print("Exception: " + str(e))
    except SystemExit as s:
        print("Exit: " + str(s))
    # At the end just close the file with the values and plot the values from it 
    finally:
        f.close()
        if(_PLOT_ENABLED_):
            plotFromFile(_PATH_FILE_)
