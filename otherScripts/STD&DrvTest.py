'''
Script used for testing standard deviation and derivative
'''

# importing the requests library
import requests
import random
import time
import pandas as pd
import math

from time import sleep
import csv

from datetime import datetime
import math

#import keyboard

from utils import Utils


# Interval to update measures
timeInterval = 0.05
dimDer = 2
dimStd = 20
dimFilter = 5
utils = Utils(dimStd, dimDer, dimFilter, timeInterval)

# Open File and write the head
f = open("MarcoRolling.csv", "w+")
writer = csv.writer(f)

# Dictionary used to store the information of the measures
values = dict(x=0.0, y=0.0, z=0.0, norm=0.0, current=0.0, roll=0.0, pitch=0.0, time=0.0, event='Still', Std_x=0.0, Std_y=0.0, Std_z=0.0, Std_norm=0.0, Std_current=0.0, Std_roll=0.0, Std_pitch=0.0, Der_x=0.0, Der_y=0.0, Der_z=0.0, Der_norm=0.0, Der_current=0.0, Der_roll=0.0, Der_pitch=0.0)

writer.writerow(values.keys())

data = pd.read_csv("../RP-A_data/test_test_MarcoRolling_RandomVelocities.csv.txt")
for index, row in data.iterrows():
    # Generate additional information about the measures
    utils.updateData(row)
    values.update(row)
    values.update(utils.calculateSTD())
    values.update(utils.calculateDerivative())

    writer.writerow(values.values())


f.close()
