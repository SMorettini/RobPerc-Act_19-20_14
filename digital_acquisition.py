'''This file contains the method to acquire the data of the current converted in digital by the Arduino'''

import RPi.GPIO as GPIO
import time
import csv

DEBUG_MODE=False

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #arduino 2 corresponding to 20 pin
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #arduino 5
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # 4
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #3

GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #arduino 2 corresponding to 2^0 pin
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #arduino 5
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # 4
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #3
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #arduino 2 corresponding to 2^0 pin
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #arduino 5

'''Function to read the data received from the Arduino and to convert them in the corrisponding value in ampere'''
def read_current():
    val = GPIO.input(17)+GPIO.input(27)*2**1+GPIO.input(22)*2**2+GPIO.input(10)*2**3+GPIO.input(9)*2**4+GPIO.input(11)*2**5+GPIO.input(5)*2**6+GPIO.input(6)*2**7+GPIO.input(13)*2**8+GPIO.input(19)*2**9

    voltage = val * (5.0 / 1023.0)

    #Sensitivity of the sensor: 625 mV/Ipn. Ipn = 50A, so the slope is 12.5 mV/A
    offset = 2.455 # Biased sensor
    val = (voltage-offset)/0.0125
    return val


#Old procedure used to test the data acquisition. Not used anymore'''
# def old_procedure():
#     try:
#         f = open("arduino.csv.txt", "w+")
#         writer = csv.writer(f)
#         head = ["value"]
#         writer.writerow(head)
#         while(True):
#             #print(GPIO.input(10))
#             # Get the value
#             val = GPIO.input(17)+GPIO.input(27)*2**1+GPIO.input(22)*2**2+GPIO.input(10)*2**3+GPIO.input(9)*2**4+GPIO.input(11)*2**5+GPIO.input(5)*2**6+GPIO.input(6)*2**7+GPIO.input(13)*2**8+GPIO.input(19)*2**9
#             writer.writerow(str(val))
#             print(str(val))
#
#             if(DEBUG_MODE):
#                 print(GPIO.input(17))
#                 print(GPIO.input(27))
#                 print(GPIO.input(22))
#                 print(GPIO.input(10))
#                 print(GPIO.input(9))
#                 print(GPIO.input(11))
#                 print(GPIO.input(5))
#                 print(GPIO.input(6))
#                 print(GPIO.input(13))
#                 print(GPIO.input(19))
#
#
#             print()
#             time.sleep(1)
#     except KeyboardInterrupt as k:
#         print("Keyboard: " + str(k))
#     except Exception as e:
#         print("Exception: " + str(e))
#     finally:
#         f.close()
