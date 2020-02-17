import pandas as pd
import numpy as np

def Sum(fileName):
    frame=pd.read_table("out/"+fileName+".csv", delimiter=",")

    frame["N_value+std+drv"] = frame["norm"] + frame["Std_norm"] + frame["Der_norm"]
    frame["N_value+std"] = frame["norm"] + frame["Std_norm"]
    frame["N_value+drv"] = frame["norm"] + frame["Der_norm"]
    frame["N_std+drv"] = frame["Std_norm"] + frame["Der_norm"]

    frame["C_value+std+drv"] = frame["current"] + frame["Std_current"] + frame["Der_current"]
    frame["C_value+std"] = frame["current"] + frame["Std_current"]
    frame["C_value+drv"] = frame["current"] + frame["Der_current"]
    frame["C_std+drv"] = frame["Std_current"] + frame["Der_current"]

    frame.to_csv("out/Sum_"+fileName+".csv")

class Utils(object):

    dimStd=0
    dimDer=0
    dimFilter=0
    dim=0
    timeInterval=0

    x = list()
    y = list()
    z = list()
    norm = list()
    current = list()
    roll = list()
    pitch = list()

    def __init__(self, dimStd, dimDer, dimFilter, timeInterval):
        self.dimStd=dimStd
        self.dimDer=dimDer
        self.dimFilter=dimFilter
        self.timeInterval=timeInterval
        self.dim=max(dimStd, dimDer+dimFilter)

        self.x = list()
        self.y = list()
        self.z = list()
        self.norm = list()
        self.current = list()
        self.roll = list()
        self.pitch = list()
        return

    def updateData(self, data):
        # Set initial data at first iteration
        if((len(self.x) < self.dim)):
            self.x.insert(0,data["x"])
            self.y.insert(0,data['y'])
            self.z.insert(0,data['z'])
            self.norm.insert(0,data['norm'])
            self.current.insert(0,data['current'])
            self.roll.insert(0,data['roll'])
            self.pitch.insert(0,data['pitch'])
        self.x.pop()
        self.x.insert(0,data['x'])
        self.y.pop()
        self.y.insert(0,data['y'])
        self.z.pop()
        self.z.insert(0,data['z'])
        self.norm.pop()
        self.norm.insert(0,data['norm'])
        self.current.pop()
        self.current.insert(0,data['current'])
        self.roll.pop()
        self.roll.insert(0,data['roll'])
        self.pitch.pop()
        self.pitch.insert(0,data['pitch'])

    def calculateSTD(self):
        values=dict()
        # If all the initial data has been added
        if((len(self.x) >= self.dimStd)):
            xA = np.asarray(self.x[0:self.dimStd])
            values["Std_x"] = np.std(xA, dtype=np.float64)

            yA = np.asarray(self.y[0:self.dimStd])
            values["Std_y"] = np.std(yA, dtype=np.float64)

            zA = np.asarray(self.z[0:self.dimStd])
            values["Std_z"] = np.std(zA, dtype=np.float64)

            normA = np.asarray(self.norm[0:self.dimStd])
            values["Std_norm"] = np.std(normA, dtype=np.float64)

            currentA = np.asarray(self.current[0:self.dimStd])
            values["Std_current"] = np.std(currentA, dtype=np.float64)

            rollA = np.asarray(self.roll[0:self.dimStd])
            values["Std_roll"] = np.std(rollA, dtype=np.float64)

            pitchA = np.asarray(self.pitch[0:self.dimStd])
            values["Std_pitch"] = np.std(pitchA, dtype=np.float64)
        return values

    def calculateDerivative(self):
        values=dict()
        start=self.calculateMA(0)
        end=self.calculateMA(self.dimDer-1)
        # If all the initial data has been added
        if((len(self.x) >= self.dimDer)):

            values["Der_x"] = (start["x"]-end["x"])/self.timeInterval/(self.dimDer-1)

            values["Der_y"] = (start["y"]-end["y"])/self.timeInterval/(self.dimDer-1)

            values["Der_z"] = (start["z"]-end["z"])/self.timeInterval/(self.dimDer-1)

            values["Der_norm"] = (start["norm"]-end["norm"])/self.timeInterval/(self.dimDer-1)

            values["Der_current"] = (start["current"]-end["current"])/self.timeInterval/(self.dimDer-1)

            values["Der_roll"] = (start["roll"]-end["roll"])/self.timeInterval/(self.dimDer-1)

            values["Der_pitch"] = (start["pitch"]-end["pitch"])/self.timeInterval/(self.dimDer-1)

        return values

    def calculateMA(self, index):
        values = dict(x=0, y=0, z=0,current=0, norm=0,  roll=0, pitch=0)
        # If all the initial data has been added
        if((len(self.x) >= self.dimFilter+index)):
            xA = np.asarray(self.x[index:self.dimFilter+index])
            values["x"] = np.ma.average(xA)

            yA = np.asarray(self.y[index:self.dimFilter+index])
            values["y"] = np.ma.average(yA)

            zA = np.asarray(self.z[index:self.dimFilter+index])
            values["z"] = np.ma.average(zA)

            normA = np.asarray(self.norm[index:self.dimFilter+index])
            values["norm"] = np.ma.average(normA)

            currentA = np.asarray(self.current[index:self.dimFilter+index])
            values["current"] = np.ma.average(currentA)

            rollA = np.asarray(self.roll[index:self.dimFilter+index])
            values["roll"] = np.ma.average(rollA)

            pitchA = np.asarray(self.pitch[index:self.dimFilter+index])
            values["pitch"] = np.ma.average(pitchA)

        return values
