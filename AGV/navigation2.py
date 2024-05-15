import RPi.GPIO as GPIO 
import time 
from line_follower_2 import *
from multiprocessing import Process, Manager
import threading

class AutonomousVehicle:
    th = None
    def __init__(self):
        self.start = ''
        self.route_plan = ''
        self.state = 'begin'
        self.status = False 
        self.current_pos_x = 990/30
        self.current_pos_y = 990/30
        self.Current_Rotation = ''
        self.AGV_status = ''
        self.Current_Rotation = 'E'
        self.PickPosition = ''
        self.th = threading.Thread(target=self.run, args=())
            
    def get_AGV_status(self):
        return self.AGV_status
    
    def set_AGV_status(self,s):
        self.AGV_status = s

    def split_string_to_list(self, input_string): 
        return input_string.split("_")
    
    def get_coordinates(self):
        return f'{self.current_pos_x*30:>03.0f}{self.current_pos_y*30:>03.0f}'
    
    def get_status(self):
        return self.status   

    def run(self):
        start_centering()
        time.sleep(1)
        done = False
        first = True
        while not done:
            if self.status:
                print("Beginning run thread")
                # Här börjar din run-funktion
                self.AGV_status = 'W'
                #global self.status
                #if start_centering:
                navigation_plan = self.split_string_to_list(self.route_plan)  # Dela upp ruttplanen i en lista 
                navigation_plan[-1] = 'F'
                print(navigation_plan)
                #start_centering()
                if first: 
                    for element in navigation_plan:
                        # Kontrollera om elementet är en koordinat (6 siffror) eller en bokstavskod (2 bokstäver)
                        #print(element)
                        #print(len(element))
                        if not self.status:
                            stop()
                            self.AGV_status = 'I'
                            self.route_plan = ''
                            remaining_plan = navigation_plan[navigation_plan.index(element)-1:]
                            for e in remaining_plan:
                                self.route_plan += str(e)
                                self.route_plan += '_'
                            self.route_plan = self.route_plan[:-1]
                            print("Pausing run thread")
                            break
                        if len(element) == 6:  # Antag att koordinater alltid har 6 siffror
                            if self.state == "begin": 
                                self.current_pos_x = int(element[:3])/30 
                                self.current_pos_y = int(element[3:])/30 
                                if self.current_pos_y == 2: 
                                    self.start = 'S' 
                                else: 
                                    self.start = 'N'
                                print("Start: ",self.start)
                                self.state = "begun"
                                next_pos_x = int(navigation_plan[navigation_plan.index(element)+1][:3])/30  # Första tre siffrorna är x-koordinaten 
                                next_pos_y = int(navigation_plan[navigation_plan.index(element)+1][3:])/30  # Sista tre siffrorna är y-koordinaten
                                print("Starting at : ",self.current_pos_x,self.current_pos_y)
                                print("Going to : ",next_pos_x,next_pos_y)
                            else:
                                next_pos_x = int(element[:3])/30  # Första tre siffrorna är x-koordinaten 
                                next_pos_y = int(element[3:])/30  # Sista tre siffrorna är y-koordinaten
                                print("At : ",self.current_pos_x,self.current_pos_y)
                                print("Going to : ",next_pos_x,next_pos_y)                

                            while self.status and (self.current_pos_x != next_pos_x or self.current_pos_y != next_pos_y):
                                #time.sleep(0.1)
                                if self.current_pos_x == next_pos_x: 
                                    if self.current_pos_y < next_pos_y:
                                        if self.Current_Rotation != 'N':
                                            #print("try to turn")
                                            rotate('N', self.Current_Rotation) # rotate and center returning Current_Rotation 
                                            self.Current_Rotation = 'N' 
                                        self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, next_pos_x, next_pos_y, False, False) # kör antal rutor 
                                    else: 
                                        if self.Current_Rotation != 'S':
                                            rotate('S', self.Current_Rotation) 
                                            self.Current_Rotation = 'S' 
                                        self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, next_pos_x, next_pos_y, False, True) 
                                elif self.current_pos_y == next_pos_y: 
                                    if self.current_pos_x < next_pos_x:
                                        if self.Current_Rotation != 'E':
                                            rotate('E', self.Current_Rotation) 
                                            self.Current_Rotation = 'E' 
                                        self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, next_pos_x, next_pos_y, True, False) 
                                    else:
                                        if self.Current_Rotation != 'W':
                                            rotate('W', self.Current_Rotation)
                                            self.Current_Rotation =  'W'
                                        self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, next_pos_x, next_pos_y, True, True)
                            #drive_centering()
                            #time.sleep(1)
                        # Just nu vill vi inte att den går in här
                        elif len(element) == 2:  # Antag att bokstavskoder alltid har 2 bokstäver
                            self.PickPosition = element
                            self.AGV_status = self.PickPosition
                            #start_centering()
                            picking(self.PickPosition, self.Current_Rotation)
                            self.AGV_status = 'W'
                            if self.PickPosition == "PN":
                                self.Current_Rotation = "N"
                            elif self.PickPosition == "PE":
                                self.Current_Rotation = "E"
                            elif self.PickPosition == "PS":
                                self.Current_Rotation = "S"
                            elif self.PickPosition == "PW":
                                self.Current_Rotation = "W"
                        elif len(element) == 1: 
                            if element == 'D': 
                                self.AGV_status = 'D'
                                picking("PW", self.Current_Rotation)
                            elif element == 'F':
                                self.AGV_status = 'F'
                                print("Status: ", self.AGV_status)
                                if self.start == 'S':
                                    rotate('S','W') 
                                    self.Current_Rotation = 'S'
                                    self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, next_pos_x, next_pos_y, False, True)
                                    self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, next_pos_x, next_pos_y, False, True)
                                else: 
                                    rotate('N','W') 
                                    self.Current_Rotation = 'N'
                                    self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, next_pos_x, next_pos_y, False, False)
                                    self.current_pos_x, self.current_pos_y = drive(self.current_pos_x, self.current_pos_y, next_pos_x, next_pos_y, False, False)
                                rotate('E', self.Current_Rotation)
                                done = True
                                return
                    #first = False    
            else:
                time.sleep(2)

    def set_status(self,new_status): 
        self.status = new_status
        if self.status and not self.th.is_alive(): 
            self.th.start()
        
    def set_route_plan(self, new_route_plan):
        self.route_plan = new_route_plan            
