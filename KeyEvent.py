# Script to update the event using the keyboard in order to classify events
import keyboard  # using module keyboard
import time

global event
event = "Still"

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


while True:  # making a loop
    print(event)
    time.sleep(.1)