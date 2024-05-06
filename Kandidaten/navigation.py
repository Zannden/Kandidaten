
from multiprocessing import Process, Value
import cam_led_detetion 
import ultrasonic
import RPi.GPIO as GPIO
import time

# ************************line follower below********************************
#left leds
GPIO.setup(26,GPIO.IN); #GDPIO -> led 1
GPIO.setup(19,GPIO.IN); #GDPIO -> led 2
GPIO.setup(13,GPIO.IN); #GDPIO -> led 3
GPIO.setup(6,GPIO.IN); #GDPIO -> led 4

#right leds
GPIO.setup(5,GPIO.IN); #GDPIO -> led 5
GPIO.setup(11,GPIO.IN); #GDPIO -> led 6
GPIO.setup(9,GPIO.IN); #GDPIO -> led 7
GPIO.setup(10,GPIO.IN); #GDPIO -> led 8

addr = 0x8  # bus address arduino
BUS = 1

bus = SMBus(BUS)  # indicates /dev/ic2-1
time.sleep(1)
# --------------------------------------------------------------------- I2C
def send_i2c_motor(cmd):
    bus.write_byte_data(addr, 0, ord(cmd[0]))
    print(f"Sent {cmd} to Arduino")

# --------------------------------------------------------------------- LED class id and state
class LED:
    def __init__(self, ID, state):
        self.ID = ID
        self.state = state
    def __str__(self):
        return f"Led: {self.ID} ({self.state})"

#addresing all leds
led1 = LED(1,"Low")
led2 = LED(2,"Low")
led3 = LED(3,"Low")
led4 = LED(4,"Low")
led5 = LED(5,"Low")
led6 = LED(6,"Low")
led7 = LED(7,"Low")
led8 = LED(8,"Low")

#array off IDs
IDs = [led1, led2, led3 ,led4 ,led5, led6 ,led7, led8]
    
def LED_state(s8,s7,s6,s5,s4,s3,s2,s1):
    L1 = 26
    L2 = 19
    L3 = 13
    L4 = 6
    L5 = 5
    L6 = 11
    L7 = 9
    L8 = 10
    
    if GPIO.input(L1)==s1 and GPIO.input(L2)==s2 and GPIO.input(L3)==s3 and GPIO.input(L4)==s4 and GPIO.input(L5)==s5 and GPIO.input(L6)==s6 and GPIO.input(L7)==s7 and GPIO.input(L8)==s8:
        return True
    else:
        return False
#*******************************************************************************

# LED setup
LED_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_pin,GPIO.OUT)

# Skapa delade minnesplatser för att lagra avstånden 
distance1 = Value('i', 0) 
distance2 = Value('i', 0) 
  
# Starta sensor-processerna 
Process(target=ultrasonic.sensor_process_1, args=(distance1,)).start() 
Process(target=ultrasonic.sensor_process_2, args=(distance2,)).start() 

# Skapa delade minnesplatser för att lagra ruttplanen och statusen
route_plan = Value('s', '')
status = Value('b', False)

# funktion för att returnera status 
def get_status():
    return status

def LED(light):
    if light:
        #tänd led
        GPIO.output(LED_pin,GPIO.HIGH)
    else: 
        #släck led
        GPIO.output(LED_pin,GPIO.LOW)

# Funktion för att dela upp strängen i en lista
def split_string_to_list(input_string):
    return input_string.split("_")

# Funktion som returnerar nuvarande koordinater
def get_coordinates(current_pos_x, current_pos_y):
    return (current_pos_x*30, current_pos_y*30)

def rotate(Rotation, Current_Rotation):

    if Rotation != Current_Rotation:
        if Rotation == 'N':
            if Current_Rotation == 'S':
                send_i2c_motor('RL')
                if LED_state(1,1,1,0,0,1,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'N'

            elif Current_Rotation == 'W':
                send_i2c_motor('RR')
                if LED_state(1,1,1,0,0,1,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'N'

            elif Current_Rotation == 'E':
                send_i2c_motor('RL')
                if LED_state(1,1,1,0,0,1,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'N'

        elif Rotation == 'S':
            if Current_Rotation == 'N':
                send_i2c_motor('RL')
                if LED_state(1,1,1,0,0,1,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'S'

            elif Current_Rotation == 'W':
                send_i2c_motor('RR')
                if LED_state(1,1,1,0,0,1,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'S'

            elif Current_Rotation == 'E':
                send_i2c_motor('RL')
                if LED_state(1,1,1,0,0,1,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'S'

        elif Rotation == 'W':
            if Current_Rotation == 'S':
                send_i2c_motor('RL')
                if LED_state(1,1,1,0,0,1,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'W'

            elif Current_Rotation == 'N':
                send_i2c_motor('RR')
                if LED_state(1,1,1,0,0,1,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'W'

            elif Current_Rotation == 'E':
                send_i2c_motor('RL')
                if LED_state(1,1,1,0,0,1,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'W'

        elif Rotation == 'E':
            if Current_Rotation == 'S':
                send_i2c_motor('RL')
                if LED_state(1,1,1,0,0,0,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'E'

            elif Current_Rotation == 'W':
                send_i2c_motor('RR')
                if LED_state(1,1,1,0,0,1,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'E'

            elif Current_Rotation == 'N':
                send_i2c_motor('RL')
                if LED_state(1,1,1,0,0,1,1,1):
                    send_i2c_motor('S')
                    Current_Rotation = 'E'

def start_centering(): 
    # Funktion för att centrera AGV på tejpen vid start
    start_centering = False
    if LED_state(1,1,1,1,0,0,1,1) or LED_state(1,1,1,1,0,0,1,1) or LED_state(1,1,1,1,1,1,0,0):
        send_i2c_motor('>')
    elif LED_state(1,1,0,0,1,1,1,1) or LED_state(1,0,0,1,1,1,1,1) or LED_state(0,0,1,1,1,1,1,1):
        send_i2c_motor('<')
    else: 
        return True

def drive_and_centering(going): # linjeföljarreglering
    while going:
        if (LED_state(1,1,1,0,0,1,1,1) or LED_state(1,1,1,1,0,1,1,1) or LED_state(1,1,1,0,1,1,1,1) and distance1 > 5):
            send_i2c_motor('F')

        elif (LED_state(1,1,0,0,1,1,1,1) or LED_state(1,1,0,1,1,1,1,1) and distance1 > 5):
            send_i2c_motor('>')

        elif (LED_state(1,1,1,1,0,0,1,1) or LED_state(1,1,1,1,1,0,1,1) and distance1 > 5):
            send_i2c_motor('<')
    
def drive(number_of_squares, current_pos_x, current_pos_y, x_dir):
    count_square = 0
    drive_and_centering(True)

    while count_square < number_of_squares:
        #middle_LED(0,1) or middle_LED(1,0) or 
        if (LED_state(0,0,0,0,0,0,0,0) or LED_state(1,1,1,1,0,0,0,0) or LED_state(0,0,0,0,1,1,1,1) and distance1 > 5):
            count_square =+ 1
            #uppdatera x eller y koordinater
            if x_dir:
                current_pos_x =+ 1
            else:
                current_pos_y =+ 1
        
        else: 
            if distance1 < 5:
                drive_and_centering(False)
                status = 'X'
                time.sleep(5)
                if distance1 > 5:
                    drive_and_centering(True)
                    status = 'W'
    
        get_coordinates(current_pos_x, current_pos_y) 

    drive_and_centering(False)

def picking(PickPostion, Current_Rotation):

    if PickPostion == 'PN':
        status = 'PN'
        rotate('N', Current_Rotation)
        if distance1 > 10:
            send_i2c_motor('F')
        if distance1 <= 5:
            send_i2c_motor('S')
        
        LED(True)
        cam_led_detection()
        LED(False)
        status = 'F'
        
    elif PickPostion == 'PS':   
        status = 'PS'
        rotate('S', Current_Rotation)
        if distance1 > 10:
            send_i2c_motor('F')
        if distance1 <= 5:
            send_i2c_motor('S')

        LED(True)
        cam_led_detection()
        LED(False)
        status = 'F'

    elif PickPostion == 'PW':
        status = 'PW'
        rotate('W', Current_Rotation) 
          if distance1 > 10:
            send_i2c_motor('FS')
            if distance1 <= 5:
                send_i2c_motor('S')

        LED(True)
        cam_led_detection()
        LED(False)
        status = 'F' 

    elif PickPostion == 'PE': 
        status = 'PW'
        roate('E', Current_Rotation)
          if distance1 > 10:
            send_i2c_motor('FS')
            if distance1 <= 5:
                send_i2c_motor('S')
        LED(True)
        cam_led_detection()
        LED(False)
        status = 'F'

# Funktion som körs i en separat process
def run():
    if start_centering():

        index = 0  # Index för att hålla reda på var vi är i navigationsplanen
        
        while True:
            if status.value:
                # Dela upp ruttplanen i en lista
                navigation_plan = split_string_to_list(route_plan.value)
                Current_Rotation = '' # east = 0, south = 1||-3, west = 2||-2, north = -1||3
                
                # Loopa igenom listan från det nuvarande indexet
                for element in navigation_plan[index:]:
                    # Kontrollera om status har ändrats till False
                    if not status.value:
                        break
                    
                    # Kontrollera om elementet är en koordinat (6 siffror) eller en bokstavskod (2 bokstäver)
                    if len(element) == 6:  # Antag att koordinater alltid har 6 siffror   

                        if index == 0:
                            current_pos_x = element[:3]/30
                            current_pos_y = element[3:]/30
                            if current_pos_x = 2:
                                start = 'S'
                            else: start = 'N'
                            
                        if index > 0:
                            current_pos_x = element[index - 1]/30 # detta är ej korrekt.
                            current_pos_y = element[index - 1]/30

                        next_pos_x = element[:3]/30  # Första tre siffrorna är x-koordinaten
                        next_pos_y = element[3:]/30  # Sista tre siffrorna är y-koordinaten

                        number_of_squares_x = abs(current_pos_x-next_pos_x)
                        number_of_squares_y = abs(current_pos_y-next_pos_y)

                        if current_pos_x == next_pos_x:
                            if current_pos_y < next_pos_y:  
                                rotate('N', Current_Rotation) # rotate and center returning Current_Rotation
                                Current_Rotation = 'N'
                                drive(number_of_squares_y, current_pos_y, current_pos_y) # kör antal rutor 
                            else: 
                                rotate('S', Current_Rotation)
                                Current_Rotation = 'S'
                                drive(number_of_squares_y)
                                
                        elif current_pos_y == next_pos_y:
                            if current_pos_x < next_pos_x:
                                rotate('E',Current_Rotation)
                                Current_Rotation = 'E'
                                drive(number_of_squares_x)

                            else: 
                                rotate('W',Current_Rotation)
                                drive(number_of_squares_x)
                                Current_Rotation = 'W'    
                    
                        print(f"Koordinat: x={x}, y={y}")

                    elif len(element) == 2:  # Antag att bokstavskoder alltid har 2 bokstäver
                        PickPostion = element
                        picking(PickPostion, Current_rotation)

                    elif len(element) == 1:
                        if element == 'D':
                            status = 'D'
                        elif element == 'F':
                            if start == 'S':
                                rotate('S','W')
                                Current_Rotation = 'S'
                            else: 
                                rotate('N','W')
                                Current_Rotation = 'N'

                            rotate('E',Current_Rotation)
                                        
                    index += 1  # Uppdatera indexet för nästa iteration
                
                time.sleep(1)

# Funktion för att starta processen
def start_navigation():
    process = Process(target=run)
    process.start()

# Funktion för att sätta ruttplanen
def set_route_plan(new_route_plan):
    route_plan.value = new_route_plan
    start_navigation()

# Funktion för att sätta statusen
def set_status(new_status):
    status.value = new_status
