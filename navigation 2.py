import RPi.GPIO as GPIO
import time
from line_follower import Driving
from multiprocessing import Process, Value

class AutonomousVehicle:
    def __init__(self, LED_pin=21):
        self.LED_pin = LED_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_pin, GPIO.OUT)
        self.route_plan = Value('s', '')
        self.status = Value('b', False)
    
    def LED(self, light):
        if light:
            GPIO.output(self.LED_pin, GPIO.HIGH)
        else:
            GPIO.output(self.LED_pin, GPIO.LOW)

    def split_string_to_list(self, input_string):
        return input_string.split("_")

    def get_coordinates(self, current_pos_x, current_pos_y):
        return (current_pos_x * 30, current_pos_y * 30)

    def run(self):
        # Här börjar din run-funktion
        if self.start_centering():
            index = 0  # Index för att hålla reda på var vi är i navigationsplanen
            
            while True:
                if self.status.value:
                    # Dela upp ruttplanen i en lista
                    navigation_plan = self.split_string_to_list(self.route_plan.value)
                    Current_Rotation = '' # east = 0, south = 1||-3, west = 2||-2, north = -1||3
                    
                    # Loopa igenom listan från det nuvarande indexet
                    for element in navigation_plan[index:]:
                        # Kontrollera om status har ändrats till False
                        if not self.status.value:
                            break
                        
                        # Kontrollera om elementet är en koordinat (6 siffror) eller en bokstavskod (2 bokstäver)
                        if len(element) == 6:  # Antag att koordinater alltid har 6 siffror   

                            if index == 0:
                                current_pos_x = int(element[:3])/30
                                current_pos_y = int(element[3:])/30
                                if current_pos_x == 2:
                                    start = 'S'
                                else: 
                                    start = 'N'
                                    
                            if index > 0:
                                current_pos_x = int(element[index - 1])/30 # detta är ej korrekt.
                                current_pos_y = int(element[index - 1])/30

                            next_pos_x = int(element[:3])/30  # Första tre siffrorna är x-koordinaten
                            next_pos_y = int(element[3:])/30  # Sista tre siffrorna är y-koordinaten

                            number_of_squares_x = abs(current_pos_x-next_pos_x)
                            number_of_squares_y = abs(current_pos_y-next_pos_y)

                            if current_pos_x == next_pos_x:
                                if current_pos_y < next_pos_y:  
                                    Driving.rotate('N', Current_Rotation) # rotate and center returning Current_Rotation
                                    Current_Rotation = 'N'
                                    Driving.drive(number_of_squares_y, current_pos_y, current_pos_y) # kör antal rutor 
                                else: 
                                    Driving.rotate('S', Current_Rotation)
                                    Current_Rotation = 'S'
                                    Driving.drive(number_of_squares_y)
                                    
                            elif current_pos_y == next_pos_y:
                                if current_pos_x < next_pos_x:
                                    Driving.rotate('E',Current_Rotation)
                                    Current_Rotation = 'E'
                                    Driving.drive(number_of_squares_x)

                                else: 
                                    Driving.rotate('W',Current_Rotation)
                                    Driving.drive(number_of_squares_x)
                                    Current_Rotation = 'W'    
                        
                            print(f"Koordinat: x={next_pos_x}, y={next_pos_y}")

                        elif len(element) == 2:  # Antag att bokstavskoder alltid har 2 bokstäver
                            PickPostion = element
                            Driving.picking(PickPostion, Current_Rotation)

                        elif len(element) == 1:
                            if element == 'D':
                                self.status = 'D'
                            elif element == 'F':
                                if start == 'S':
                                    Driving.rotate('S','W')
                                    Current_Rotation = 'S'
                                else: 
                                    Driving.rotate('N','W')
                                    Current_Rotation = 'N'

                                Driving.rotate('E',Current_Rotation)
                                            
                        index += 1  # Uppdatera indexet för nästa iteration
                    
                    time.sleep(1)
        # Här slutar din run-funktion
                
    def start_navigation(self):
        process = Process(target=self.run)
        process.start()

    def set_route_plan(self, new_route_plan):
        self.route_plan.value = new_route_plan
        self.start_navigation()

    def set_status(self, new_status):
        self.status.value = new_status