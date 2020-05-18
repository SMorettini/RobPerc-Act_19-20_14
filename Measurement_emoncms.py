'''
This file contains a working variant of Measurement.py for storing the data on a web server
in real time.

It needs to be updated with the state machine and the new features evaluated using utils.py.
Now for the detection of the state only a simple threshold method is used.
'''

import smbus
from time import sleep,time
import csv

from datetime import datetime

import math

# select the correct i2c bus for this revision of Raspberry Pi
revision = ([l[12:-1] for l in open('/proc/cpuinfo',
                                    'r').readlines() if l[:8] == "Revision"]+['0000'])[0]
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


if __name__ == "__main__":
    # if run directly we'll just create an instance of the class and output
    # the current readings
    adxl345 = ADXL345()
    i = 0
    x, y, z, norm, roll, pitch, event, Vx, Vy, Vz = 0
    timeInterval = 0.05
    alpha = 0.5
    apikey = "99c785a9f562fa18d8b475aeb58b1648"
    try:
        f = open("test.csv.txt", "w+")
        writer = csv.writer(f)
        head = ["x","y","z","norm","roll","pitch","event","time"]
        writer.writerow(head)
        while(True):
            # Get value from accelerometer
            axes = adxl345.getAxes(True)

            # Calculate additional information about the sensors measurement
            axes["time"] = datetime.now()
            axes['norm'] = math.sqrt((axes['x'] * axes['x']) + (axes['y'] * axes['y']) + (axes['z'] * axes['z']))
            axes['roll'] = math.atan2(axes['y'], axes['z']) * 180 / math.pi
            axes['pitch'] = math.atan2(-1*axes['x'], math.sqrt(axes['y']*axes['y']+axes['z']*axes['z'])) * 180 / math.pi

            # Set initial data at first iteration
            if(i==0):
                x = axes['x']
                y = axes['y']
                z = axes['z']
                norm = axes['norm']
                roll = axes['roll']
                pitch = axes['pitch']
            # Low Pass Filter to smooth out data
            x = axes['x'] * alpha + (x * (1.0 - alpha))
            y = axes['y'] * alpha + (y * (1.0 - alpha))
            z = axes['z'] * alpha + (z * (1.0 - alpha))
            norm = axes['norm'] * alpha + (norm * (1.0 - alpha))
            roll = axes['roll'] * alpha + (roll * (1.0 - alpha))
            pitch = axes['pitch'] * alpha + (pitch * (1.0 - alpha))
            # Calculate velocity discretely
            Vx = Vx + timeInterval * x
            Vy = Vy + timeInterval * y
            Vz = Vz + timeInterval * z


            # Check for the event [TODO] take into account also roll, pitch, mean, std, ...
            axes["event"] = 0#"WOW"
            if(1.1 < axes['norm'] < 2):
                axes['event'] = 0#"Machine Learning detected: Moving"
            elif(0.9 <= axes['norm'] <= 1.1):
                axes['event'] = 0#"Machine Learning detected: Still"
            elif(axes['norm'] >= 2):
                axes['event'] = 1#"Machine Learning detected: Crash"
            else:#<0.9
                axes['event'] = 0#"Machine Learning detected: Mars"

            # Print to csv
            writer.writerow(axes.values())

            # api-endpoint
            if(i % 50 == 0):
                date = time.time()
                URL = "https://emoncms.org/input/post?node=1&time=" + str(date) +"&csv=" + "x:"+str(x) + "," + "y:"+str(y) + "," + "z:"+str(axes["z"]) + "," + "norm:"+str(axes["norm"]) + "," + "roll:"+str(axes["roll"]) + "," + "pitch:"+str(axes["pitch"]) + "," + "event:"+str(axes["event"].split(":")[-1]) + "&apikey=" + apikey
                # Reset index to reset low pass filter
                i = 0

            # Wait and update index
            sleep(timeInterval)
            i += 1


    except KeyboardInterrupt as k:
        print("Keyboard: " + str(k))
    except Exception as e:
        print("Exception: " + str(e))
    finally:
        f.close()
