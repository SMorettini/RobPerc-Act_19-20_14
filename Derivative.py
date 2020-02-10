# Import libraries
import time
import pandas as pd

import csv
from numpy import diff

i = 0
x = list()
y = list()
z = list()
norm = list()
current = list()
roll = list()
pitch = list()
event = list()
timeInterval = 0.05
dimension = 2

values = dict(x=0, y=0, z=0,current=0, norm=0,  roll=0, pitch=0, time=0)


def calculateDerivative(index, data, timeInterval, dimension):
    # Set initial data at first iteration
    if((index < dimension)):
        x.insert(0,data['x'])
        y.insert(0,data['y'])
        z.insert(0,data['z'])
        norm.insert(0,data['norm'])
        current.insert(0,data['current'])
        roll.insert(0,data['roll'])
        pitch.insert(0,data['pitch'])
    x.pop()
    x.insert(0,data['x'])
    y.pop()
    y.insert(0,data['y'])
    z.pop()
    z.insert(0,data['z'])
    norm.pop()
    norm.insert(0,data['norm'])
    current.pop()
    current.insert(0,data['current'])
    roll.pop()
    roll.insert(0,data['roll'])
    pitch.pop()
    pitch.insert(0,data['pitch'])

    # If all the initial data has been added
    if((index >= dimension)):
        values["x"] = (x[0]-x[dimension-1])/timeInterval/(dimension-1)

        values["y"] = (y[0]-y[dimension-1])/timeInterval/(dimension-1)

        values["z"] = (z[0]-z[dimension-1])/timeInterval/(dimension-1)

        values["norm"] = (norm[0]-norm[dimension-1])/timeInterval/(dimension-1)

        values["current"] = (current[0]-current[dimension-1])/(dimension-1)

        values["roll"] = (roll[0]-roll[dimension-1])/timeInterval/(dimension-1)

        values["pitch"] = (pitch[0]-pitch[dimension-1])/timeInterval/(dimension-1)

        
    # Set the time as the latest one
    values["time"] = row["time"]

    return values


try:
    f = open("Derivative_test_test_HoldingAndBumpingAndCrash_RandomVelocities.csv.txt", "w+")
    writer = csv.writer(f)
    writer.writerow(values.keys())

    data = pd.read_csv("../RP-A_data/test_test_HoldingAndBumpingAndCrash_RandomVelocities.csv.txt")
    for index, row in data.iterrows():
        values = calculateDerivative(index, row, timeInterval, dimension)

        writer.writerow(values.values())

        #print(values)

        # Wait and update index
        #time.sleep(timeInterval)


except KeyboardInterrupt as k:
    print("Keyboard: " + str(k))
except Exception as e:
    print("Exception: " + str(e))
except SystemExit as s:
    print("Exit: " + str(s))
finally:
    f.close()
