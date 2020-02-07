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

values = dict(x=0, y=0, z=0,current=0, norm=0,  roll=0, pitch=0, time=0)


def calculateSTD(index, data):
    # Set initial data at first iteration
    if((index < 20)): 
        x.append(data['x'])
        y.append(data['y'])
        z.append(data['z'])
        norm.append(data['norm'])
        current.append(data['current'])
        roll.append(data['roll'])
        pitch.append(data['pitch'])
    x.pop()
    x.append(data['x'])
    y.pop()
    y.append(data['y'])
    z.pop()
    z.append(data['z'])
    norm.pop()
    norm.append(data['norm'])
    current.pop()
    current.append(data['current'])
    roll.pop()
    roll.append(data['roll'])
    pitch.pop()
    pitch.append(data['pitch'])

    # If all the initial data has been added
    if((index >= 20)): 
        xA = np.asarray(x)
        values["x"] = np.std(xA, dtype=np.float64)

        yA = np.asarray(y)
        values["y"] = np.std(yA, dtype=np.float64)

        zA = np.asarray(z)
        values["z"] = np.std(zA, dtype=np.float64)

        normA = np.asarray(norm)
        values["norm"] = np.std(normA, dtype=np.float64)

        currentA = np.asarray(current)
        values["current"] = np.std(currentA, dtype=np.float64)

        rollA = np.asarray(roll)
        values["roll"] = np.std(rollA, dtype=np.float64)

        pitchA = np.asarray(pitch)
        values["pitch"] = np.std(pitchA, dtype=np.float64)

        # Set the time as the latest one
        values["time"] = row["time"]

    return values


try:
    f = open("crash_STD1.csv.txt", "w+")
    writer = csv.writer(f)
    writer.writerow(values.keys())

    data = pd.read_csv("data/fullTest.csv.txt")
    for index, row in data.iterrows():
        values = calculateSTD(index, row)


        writer.writerow(values.values())

        #print(values)

        # Wait and update index
        time.sleep(timeInterval)


except KeyboardInterrupt as k:
    print("Keyboard: " + str(k))
except Exception as e:
    print("Exception: " + str(e))
except SystemExit as s:
    print("Exit: " + str(s))
finally:
    f.close()