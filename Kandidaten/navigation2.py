import RPi.GPIO as GPIO 
import time 
from line_follower_2 import *
from multiprocessing import Process, Manager

class AutonomousVehicle: 
    def __init__(self, LED_pin=21): 
        self.LED_pin = LED_pin 
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.LED_pin, GPIO.OUT) 
        self.route_plan = '' 
        self.status = False 
        self.current_pos_x = 0
        self.current_pos_y = 0
        self.Current_Rotation = ''
        self.AGV_status = ''
        self.Current_Rotation = 'E'
        
    def LED(self, light): 
        if light: 
            GPIO.output(self.LED_pin, GPIO.HIGH) 
        else: 
            GPIO.output(self.LED_pin, GPIO.LOW)
            
    def get_AGV_status(self):
        return self.AGV_status

    def split_string_to_list(self, input_string): 
        return input_string.split("_")
    
    def get_coordinates(self):
        return '{:03d}{:03d}'.format(self.current_pos_x*30, self.current_pos_y*30)

    def run(self): 
        # Här börjar din run-funktion
        self.AGV_status = 'W'
        #if start_centering:
        navigation_plan = self.split_string_to_list(self.route_plan)  # Dela upp ruttplanen i en lista 
        index = 0 # Index för att hålla reda på var vi är i navigationsplanen
        for element in navigation_plan:
            # Kontrollera om elementet är en koordinat (6 siffror) eller en bokstavskod (2 bokstäver)
            print(element)
            print(len(element))
            if len(element) == 6:  # Antag att koordinater alltid har 6 siffror
                if index == 0: 
                    self.current_pos_x = int(element[:3])/30 
                    self.current_pos_y = int(element[3:])/30 
                    if self.current_pos_y == 2: 
                        start = 'S' 
                    else: 
                        start = 'N' 
                next_pos_x = int(element[:3])/30  # Första tre siffrorna är x-koordinaten 
                next_pos_y = int(element[3:])/30  # Sista tre siffrorna är y-koordinaten
                print(self.current_pos_x,self.current_pos_y)
                print(next_pos_x,next_pos_y)                

                while self.status and (self.current_pos_x != next_pos_x or self.current_pos_y != next_pos_y):
                    time.sleep(0.1)
                    if self.current_pos_x == next_pos_x: 
                        if self.current_pos_y < next_pos_y:
                            if self.Current_Rotation != 'N':
                                #print("try to turn")
                                rotate('N', self.Current_Rotation) # rotate and center returning Current_Rotation 
                                self.Current_Rotation = 'N' 
                            self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, False, False) # kör antal rutor 
                        else: 
                            if self.Current_Rotation != 'S':
                                rotate('S', self.Current_Rotation) 
                                self.Current_Rotation = 'S' 
                            self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, False, True) 
                    elif self.current_pos_y == next_pos_y: 
                        if self.current_pos_x < next_pos_x:
                            if self.Current_Rotation != 'E':
                                rotate('E', self.Current_Rotation) 
                                self.Current_Rotation = 'E' 
                            self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, True, False) 
                        else:
                            if self.Current_Rotation != 'W':
                                rotate('W', self.Current_Rotation)
                                self.Current_Rotation = 'W' 
                            self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, True, True)
                            
            # Just nu vill vi inte att den går in här
            elif len(element) == 2:  # Antag att bokstavskoder alltid har 2 bokstäver
                PickPostion = element
                self.AGV_status = PickPosition
                picking(PickPostion, self.Current_Rotation)
                self.AGV_status = 'W'
            elif len(element) == 1: 
                if element == 'D': 
                    self.status = 'D' 
                elif element == 'F': 
                    if start == 'S': 
                        rotate('S','W') 
                        self.Current_Rotation = 'S'
                        drive(self.current_pos_x, self.current_pos_y, False)
                    else: 
                        rotate('N','W') 
                        self.Current_Rotation = 'N'
                        drive(self.current_pos_x, self.current_pos_y, False)
                    rotate('E', self.Current_Rotation) 
            index += 1  # Uppdatera indexet för nästa iteration 

    def set_status(self,new_status): 
        self.status = new_status
        if self.status:
            process = Process(target=self.run) 
            process.start()
        
    def set_route_plan(self, new_route_plan):
        self.route_plan = new_route_plan            