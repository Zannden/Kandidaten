from multiprocessing import Process, Value
from ultrasonic import *
import RPi.GPIO as GPIO
import time
from smbus import SMBus
#import IR_LED_GUI
GPIO.setmode(GPIO.BCM)
# --------------------------------I2C------------------------------------
addr = 0x8  # bus address arduino
BUS = 1

bus = SMBus(BUS)  # indicates /dev/ic2-1
time.sleep(1)

def send_i2c_motor(cmd):
    bus.write_byte_data(addr, 0, ord(cmd[0]))
    time.sleep(0.01)
    #print(f"Sent {cmd} to Arduino")

# --------------------------ultrasonic---------------------------------
# Skapa delade minnesplatser för att lagra avstånden 
#distance1 = Value('i', 0) 
#distance2 = Value('i', 0) 
  
# Starta sensor-processerna 
#Process(target=ultrasonic.sensor_process_1, args=(distance1,)).start() 
#Process(target=ultrasonic.sensor_process_2, args=(distance2,)).start() 

# -------------------------line follower--------------------------------
# left leds
GPIO.setup(26, GPIO.IN)  # GPIO -> led 1
GPIO.setup(19, GPIO.IN)  # GPIO -> led 2
GPIO.setup(13, GPIO.IN)  # GPIO -> led 3
GPIO.setup(6, GPIO.IN)   # GPIO -> led 4

# right leds
GPIO.setup(5, GPIO.IN)   # GPIO -> led 5
GPIO.setup(11, GPIO.IN)  # GPIO -> led 6
GPIO.setup(9, GPIO.IN)   # GPIO -> led 7
GPIO.setup(10, GPIO.IN)  # GPIO -> led 8
# --------------------------------------------------------------------- LED class id and state
class LED:
    def __init__(self, ID, state):
        self.ID = ID
        self.state = state

    def __str__(self):
        return f"Led: {self.ID} ({self.state})"

# addressing all leds
led1 = LED(1, "Low")
led2 = LED(2, "Low")
led3 = LED(3, "Low")
led4 = LED(4, "Low")
led5 = LED(5, "Low")
led6 = LED(6, "Low")
led7 = LED(7, "Low")
led8 = LED(8, "Low")

# array off IDs
IDs = [led1, led2, led3, led4, led5, led6, led7, led8]
    
def LED_state(s8, s7, s6, s5, s4, s3, s2, s1):
    L1 = 26
    L2 = 19
    L3 = 13
    L4 = 6
    L5 = 5
    L6 = 11
    L7 = 9
    L8 = 10
    
    if GPIO.input(L1) == s1 and GPIO.input(L2) == s2 and GPIO.input(L3) == s3 and GPIO.input(L4) == s4 and GPIO.input(L5) == s5 and GPIO.input(L6) == s6 and GPIO.input(L7) == s7 and GPIO.input(L8) == s8:
        return True
    else:
        return False
# --------------------------------------------------------------------------------------

def rotate(Rotation, Current_Rotation):
    print('Rotating')
    print(Current_Rotation, Rotation)
    
    while Rotation != Current_Rotation:
        Next_Rotation = Rotation
        no_tape = False
        find_tape = False
        if Rotation == 'N':
            if Current_Rotation == 'S':
                send_i2c_motor('L')
                Next_Rotation = 'E'

            elif Current_Rotation == 'W':
                send_i2c_motor('R')

            elif Current_Rotation == 'E':
                send_i2c_motor('L')

        elif Rotation == 'S':
            if Current_Rotation == 'N':
                send_i2c_motor('L')
                Next_Rotation = 'W'

            elif Current_Rotation == 'W':
                send_i2c_motor('L')

            elif Current_Rotation == 'E':
                send_i2c_motor('R')

        elif Rotation == 'W':
            if Current_Rotation == 'S':
                send_i2c_motor('R')

            elif Current_Rotation == 'N':
                send_i2c_motor('L')

            elif Current_Rotation == 'E':
                send_i2c_motor('L')
                Next_Rotation = 'N'
        
        elif Rotation == 'E':
            if Current_Rotation == 'S':
                send_i2c_motor('L')

            elif Current_Rotation == 'W':
                send_i2c_motor('L')
                Next_Rotation = 'S'

            elif Current_Rotation == 'N':
                send_i2c_motor('R')
        
        while Next_Rotation != Current_Rotation:
            if find_tape and (LED_state(1, 1, 1, 0, 0, 1, 1, 1) or LED_state(1, 1, 1, 0, 1, 1, 1, 1) or LED_state(1, 1, 1, 1, 0, 1, 1, 1) or LED_state(1, 1, 1, 1, 0, 1, 1, 1)):
                send_i2c_motor('S')
                Current_Rotation = Next_Rotation
            if no_tape and (LED_state(0, 0, 1, 1, 1, 1, 1, 1) or LED_state(0, 1, 1, 1, 1, 1, 1, 1) or LED_state(1, 1, 1, 1, 1, 1, 1, 0) or LED_state(1, 1, 1, 1, 1, 1, 0, 0)) or LED_state(1, 0, 1, 1, 1, 1, 1, 1) or LED_state(1, 1, 1, 1, 1, 1, 0, 1):
                find_tape = True
            elif (LED_state(1,1,1,1,1,1,1,1)):
                no_tape = True
        

def start_centering(): 
    # Funktion för att centrera AGV på tejpen vid start
    start_centering = False
    if LED_state(1, 1, 1, 1, 0, 0, 1, 1) or LED_state(1, 1, 1, 1, 0, 0, 1, 1) or LED_state(1, 1, 1, 1, 1, 1, 0, 0):
        send_i2c_motor('>')
        if LED_state(1, 1, 1, 0, 0, 1, 1, 1) or LED_state(1, 1, 1, 0, 1, 1, 1, 1) or LED_state(1, 1, 1, 1, 0, 1, 1, 1):
            send_i2c_motor('S')
            time.sleep(5)
            start_centering = True
    elif LED_state(1, 1, 0, 0, 1, 1, 1, 1) or LED_state(1, 0, 0, 1, 1, 1, 1, 1) or LED_state(0, 0, 1, 1, 1, 1, 1, 1):
        send_i2c_motor('<')
        if LED_state(1, 1, 1, 0, 0, 1, 1, 1) or LED_state(1, 1, 1, 0, 1, 1, 1, 1) or LED_state(1, 1, 1, 1, 0, 1, 1, 1):
            send_i2c_motor('S')
            time.sleep(5)
            start_centering = True
    return start_centering

def drive(current_pos_x, current_pos_y, x_dir, neg_dir):
    print("driving")
    while True:
        if (LED_state(1, 1, 1, 0, 0, 1, 1, 1) or LED_state(1, 1, 1, 1, 0, 1, 1, 1) or LED_state(1, 1, 1, 0, 1, 1, 1, 1)): #and distance1 > 5:
            send_i2c_motor('F')
        elif (LED_state(1, 1, 0, 0, 1, 1, 1, 1) or LED_state(1, 1, 0, 1, 1, 1, 1, 1) or LED_state(1, 0, 0, 1, 1, 1, 1, 1) or LED_state(1, 0, 1, 1, 1, 1, 1, 1) or LED_state(0, 0, 1, 1, 1, 1, 1, 1) or LED_state(0, 1, 1, 1, 1, 1, 1, 1)): #and distance1 > 5:
            send_i2c_motor('D')
        elif (LED_state(1, 1, 1, 1, 0, 0, 1, 1) or LED_state(1, 1, 1, 1, 1, 0, 1, 1) or LED_state(1, 1, 1, 1, 1, 0, 0, 1) or LED_state(1, 1, 1, 1, 1, 1, 0, 1) or LED_state(1, 1, 1, 1, 1, 1, 0, 0) or LED_state(1, 1, 1, 1, 1, 1, 1, 0)): #and distance1 > 5:
            send_i2c_motor('A')
        elif (LED_state(0, 0, 0, 0, 0, 0, 0, 0) or LED_state(1, 1, 1, 1, 0, 0, 0, 0) or LED_state(0, 0, 0, 0, 1, 1, 1, 1) or LED_state(1,0,0,0,0,1,1,1) or LED_state(1,1,0,0,0,0,1,1) or  LED_state(1,1,1,0,0,0,0,1) or LED_state(0,0,0,1,1,1,1,1) or LED_state(1,1,1,1,1,0,0,0)): #and distance1 > 5:
            time.sleep(0.4)
            send_i2c_motor('S')
            if x_dir and not neg_dir:
                current_pos_x += 1
            elif not x_dir and not neg_dir:
                current_pos_y += 1
            elif x_dir and neg_dir:
                current_pos_x -= 1
            else:
                current_pos_y -= 1
            break
               #else: 
            #if distance1 < 5:
            #    drive_and_centering(False)
            #    status = 'X'
             #   time.sleep(5)
                #if distance1 > 5:
                #    drive_and_centering(True)
                #    status = 'W'
    #print(current_pos_x,current_pos_y)
    return current_pos_x, current_pos_y

def picking(PickPostion, Current_Rotation):
    if PickPostion == 'PN':
        rotate('N', Current_Rotation)
        time.sleep(2)
        start_dist = sensor_process_1() # Spara original distansen till kuben
        while sensor_process_1() > 6: # Kör fram till vi är nära kuben
            send_i2c_motor('F')
        send_i2c_motor('S')
        #Blinka LEDs och vänta
        LED(True)
        time.sleep(5)
        #cam_led_detection()
        LED(False)
        while sensor_process_1() < start_dist: # Backa tills vi är på original distansen
            send_i2c_motor('B')
        send_i2c_motor('S')
        
        
        
    elif PickPostion == 'PS':   
        rotate('S', Current_Rotation)
        time.sleep(2)
        start_dist = sensor_process_1() # Spara original distansen till kuben
        while sensor_process_1() > 6: # Kör fram till vi är nära kuben
            send_i2c_motor('F')
        send_i2c_motor('S')
        #Blinka LEDs och vänta
        LED(True)
        time.sleep(5)
        #cam_led_detection()
        LED(False)
        while sensor_process_1() < start_dist: # Backa tills vi är på original distansen
            send_i2c_motor('B')
        send_i2c_motor('S')

    elif PickPostion == 'PW':
        rotate('W', Current_Rotation) 
        time.sleep(2)
        start_dist = sensor_process_1() # Spara original distansen till kuben
        while sensor_process_1() > 6: # Kör fram till vi är nära kuben
            send_i2c_motor('F')
        send_i2c_motor('S')
        #Blinka LEDs och vänta
        LED(True)
        time.sleep(5)
        #cam_led_detection()
        LED(False)
        while sensor_process_1() < start_dist: # Backa tills vi är på original distansen
            send_i2c_motor('B')
        send_i2c_motor('S')

    elif PickPostion == 'PE': 
        rotate('E', Current_Rotation)
        time.sleep(2)
        start_dist = sensor_process_1() # Spara original distansen till kuben
        while sensor_process_1() > 6: # Kör fram till vi är nära kuben
            send_i2c_motor('F')
        send_i2c_motor('S')
        #Blinka LEDs och vänta
        LED(True)
        time.sleep(5)
        #cam_led_detection()
        LED(False)
        while sensor_process_1() < start_dist: # Backa tills vi är på original distansen
            send_i2c_motor('B')
        send_i2c_motor('S')

