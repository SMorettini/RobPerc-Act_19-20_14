'''Script used to test the upload of the data on emocms, a web service for storing and visualizing data in a dashboard'''

# importing the requests library
import requests
import random
import time
import pandas as pd
import math
import numpy as np

apikey = "99c785a9f562fa18d8b475aeb58b1648"
i = 0
x = list()
y = list()
z = list()
norm = list()
roll = list()
pitch = list()
event = list()
timeInterval = 0.05

data = pd.read_csv("crash.csv")
for index, row in data.iterrows():
    # Set initial data at first iteration
    if((index < 100)):
        x.append(row['x'])
        y.append(row['y'])
        z.append(row['z'])
        norm.append(row['norm'])
        roll.append(row['roll'])
        pitch.append(row['pitch'])
    x.pop()
    x.append(row['x'])
    y.pop()
    y.append(row['y'])
    z.pop()
    z.append(row['z'])
    norm.pop()
    norm.append(row['norm'])
    roll.pop()
    roll.append(row['roll'])
    pitch.pop()
    pitch.append(row['pitch'])

    # api-endpoint
    if(index % 100 == 0):
        timestamp = time.time() -2.5

        print(timestamp)

        normA = np.asarray(norm)
        normV = np.ma.average(normA)

        xA = np.asarray(x)
        xV = np.ma.average(xA)

        yA = np.asarray(y)
        yV = np.ma.average(yA)

        zA = np.asarray(z)
        zV = np.ma.average(zA)

        rollA = np.asarray(roll)
        rollV = np.ma.average(rollA)

        pitchA = np.asarray(pitch)
        pitchV = np.ma.average(pitchA)

        URL = "https://emoncms.org/input/post?node=2&time=" + str(timestamp) +"&csv=" + "x:"+str(xV) + "," + "y:"+str(yV) + "," + "z:"+str(zV) + "," + "norm:"+str(normV) + "," + "roll:"+str(rollV) + "," + "pitch:"+str(pitchV) + "," + "event:"+str(event) + "&apikey=" + apikey

        # sending get request and saving the response as response object
        r = requests.get(url = URL)

    # Wait and update index
    time.sleep(timeInterval)
