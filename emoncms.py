'''Script used to test the upload of the data on emocms, a web service for storing and visualizing data in a dashboard'''
import requests
import random
import time
import pandas as pd
import math

apikey = "99c785a9f562fa18d8b475aeb58b1648"
"""
for index, row in data.iterrows():
    x = row["x"]
    y = row["y"]
    z = row["z"]

    # api-endpoint 
    date = time.time()
    URL = "https://emoncms.org/input/post?node=1&time=" + str(date) +"&csv=" + "x:"+str(row["x"]) + "," + "y:"+str(row["y"]) + "," + "z:"+str(row["z"]) + "," + "norm:"+str(row["norm"]) + "," + "roll:"+str(row["roll"]) + "," + "pitch:"+str(row["pitch"]) + "," + "event:"+str(row["event"].split(":")[-1]) + "&apikey=" + apikey
    print(str(date) + " "+str(row["event"].split(":")[-1]))
    # sending get request and saving the response as response object
    r = requests.get(url = URL)

    time.sleep(5)

"""
i = 0
x = 0
y = 0
z = 0
norm = 0
roll = 0
pitch = 0
event = 0
alpha = 0.25
timeInterval = 0.5
apikey = "99c785a9f562fa18d8b475aeb58b1648"

Vx = 0
Vy = 0
Vz = 0

data = pd.read_csv("crash.csv")
for index, row in data.iterrows():
    # Set initial data at first iteration
    if((index == 0) or ((index-1) % 10 == 0)):
        x = row['x']
        y = row['y']
        z = row['z']
        norm = row['norm']
        roll = row['roll']
        pitch = row['pitch']
    # Low Pass Filter to smooth out data
    x = row['x'] * alpha + (x * (1.0 - alpha))
    y = row['y'] * alpha + (y * (1.0 - alpha))
    z = row['z'] * alpha + (z * (1.0 - alpha))
    norm = row['norm'] * alpha + (norm * (1.0 - alpha))
    roll = row['roll'] * alpha + (roll * (1.0 - alpha))
    pitch = row['pitch'] * alpha + (pitch * (1.0 - alpha))

    # Calculate velocity discretely
    Vx = Vx + timeInterval * x
    Vy = Vy + timeInterval * y
    Vz = Vz + timeInterval * z



    # Check for the event [TODO] take into account also roll, pitch, mean, std, ...
    event = 0#"WOW"
    if(1.2 <= norm <= 1.8):
        event = 0#"Machine Learning detected: Moving"
    elif(0.8 < norm < 1.2):
        event = 0#"Machine Learning detected: Still"
    elif(norm > 2):
        event = 1#"Machine Learning detected: Crash"
    else:
        event = 0#"Machine Learning detected: Mars"


    # api-endpoint
    if(index % 10 == 0):
        date = time.time()

        Vel = math.sqrt(Vx*Vx + Vy*Vy + Vz*Vz)
        print(Vel)

        URL = "https://emoncms.org/input/post?node=1&time=" + str(date) +"&csv=" + "x:"+str(x) + "," + "y:"+str(y) + "," + "z:"+str(row["z"]) + "," + "norm:"+str(row["norm"]) + "," + "roll:"+str(row["roll"]) + "," + "pitch:"+str(row["pitch"]) + "," + "event:"+str(row["event"].split(":")[-1]) + ",vel:" +str(Vel) + ",vx:" +str(Vx) + ",vy:" +str(Vy) + ",vz:" +str(Vz) + "&apikey=" + apikey

        # sending get request and saving the response as response object
        r = requests.get(url = URL)

    # Wait and update index
    time.sleep(timeInterval)
