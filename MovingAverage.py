# importing the requests library
import requests
import random
import time
import pandas as pd
import math
import numpy as np

import csv

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
dimension = 5

values = dict(x=0, y=0, z=0,current=0, norm=0,  roll=0, pitch=0, time=0)


def calculateMA(index, data, dimension):
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
        xA = np.asarray(x)
        values["x"] = np.ma.average(xA)

        yA = np.asarray(y)
        values["y"] = np.ma.average(yA)

        zA = np.asarray(z)
        values["z"] = np.ma.average(zA)

        normA = np.asarray(norm)
        values["norm"] = np.ma.average(normA)

        currentA = np.asarray(current)
        values["current"] = np.ma.average(currentA)

        rollA = np.asarray(roll)
        values["roll"] = np.ma.average(rollA)

        pitchA = np.asarray(pitch)
        values["pitch"] = np.ma.average(pitchA)

    # Set the time as the latest one
    values["time"] = row["time"]

    return values


try:
    f = open("../RP-A_data/MA_MarcoRolling_RandomVelocities.csv.txt", "w+")
    writer = csv.writer(f)
    writer.writerow(values.keys())

    data = pd.read_csv("../RP-A_data/test_test_MarcoRolling_RandomVelocities.csv.txt")
    for index, row in data.iterrows():
        values = calculateMA(index, row, dimension)

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
