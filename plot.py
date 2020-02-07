import plotly
import chart_studio.plotly as py
import plotly.graph_objs as go

import pandas as pd

def plotData(data, message='Data', s=None, e=None):
    print("Plotting")
    dataG= []

    for key in data.columns.values:
        if(key!="time"):
            if(key!="event"):
                if(key=="current"):
                    dataG.append(go.Scatter(y=data[key][s:e],
                                    x=data["time"][s:e],
                                    yaxis='y2',
                                    name=key))
                else:
                    dataG.append(go.Scatter(y=data[key][s:e],
                                    x=data["time"][s:e],
                                    name=key))

    layout = dict(
        title=message,
        width=1000,
        height=450,
        xaxis=dict(
            rangeselector=dict(),
            rangeslider=dict()
        ),
        yaxis=dict(
            title='0 to 1'
        ),
        yaxis2=dict(
            title='current',
            overlaying='y',
            side='right'
        )
    )
    fig = dict(data=dataG, layout=layout)
    plotly.offline.plot(fig, auto_open=True)

def plotFromFile(path):
    frame=pd.read_table(path, delimiter=",")
    plotData(frame)

#plotFromFile('RP-A_data/test_softCrashChair_LowestVelocities.csv.txt')
