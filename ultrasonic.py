import RPi.GPIO as GPIO 
import time 
from multiprocessing import Value

# Definiera GPIO-pinnar för ultraljudssensorerna 
TRIG1 = 24
ECHO1 = 23
TRIG2 = 8
ECHO2 = 25 

# Sätt upp GPIO-pinnarna 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(TRIG1, GPIO.OUT) 
GPIO.setup(ECHO1, GPIO.IN) 
GPIO.setup(TRIG2, GPIO.OUT) 
GPIO.setup(ECHO2, GPIO.IN) 

def read_sensor(TRIG, ECHO): 
    # Skicka ut en trigger-puls 
    GPIO.output(TRIG, True) 
    time.sleep(0.00001) 
    GPIO.output(TRIG, False) 

    # Vänta på att ekot ska börja 
    while GPIO.input(ECHO) == 0: 
        pass 
    start = time.time() 

    # Vänta på att ekot ska sluta 
    while GPIO.input(ECHO) == 1: 
        pass 
    end = time.time() 

    # Beräkna avståndet baserat på tiden det tog för ekot att återvända 
    distance = (end - start) * 34300 / 2 
    return distance 

def sensor_process_1(distance1):
    while True: 
        distance1.value = read_sensor(TRIG1, ECHO1)
        time.sleep(0.1)

def sensor_process_2(distance2):
    while True: 
        distance2.value = read_sensor(TRIG2, ECHO2)
        time.sleep(0.1)