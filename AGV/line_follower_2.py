from multiprocessing import Process, Value
from ultrasonic import *
import RPi.GPIO as GPIO
import time
from smbus import SMBus
from led_detection import *
#import IR_LED_GUI
GPIO.setmode(GPIO.BCM)
# --------------------------------I2C------------------------------------
addr = 0x8  # bus address arduino
BUS = 1

bus = SMBus(BUS)  # indicates /dev/ic2-1
time.sleep(1)

# Skickar kommandon till Arduino
def send_i2c_motor(cmd):
    while True:
        #time.sleep(0.01)
        try:
            bus.write_byte_data(addr, 0, ord(cmd[0]))
            break
        except:
            print("Error in sending")
    # En viss delay behövs just nu för att vi inte ska fä en I2C krash ibland, när data skickas för fort
    # Dock så ger en högre delay ojämnare körning hos AGVn. Detta behöver lösas och har ganksa hög PRIO
    #print(f"Sent {cmd} to Arduino")


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

GPIO.setup(17, GPIO.IN)   # GPIO -> led 9
GPIO.setup(27, GPIO.IN)  # GPIO -> led 10

GPIO.output(8, GPIO.LOW) # Stäng av LED lyslampan 

L1 = 26
L2 = 19
L3 = 13
L4 = 6
L5 = 5
L6 = 11
L7 = 9
L8 = 10
L9 = 17
L10 = 27

# Ger True om statet man skickar in stämmer med vad IR sensorerna känner av
def LED_front(s8, s7, s6, s5, s4, s3, s2, s1):
    
    if GPIO.input(L1) == s1 and GPIO.input(L2) == s2 and GPIO.input(L3) == s3 and GPIO.input(L4) == s4 and GPIO.input(L5) == s5 and GPIO.input(L6) == s6 and GPIO.input(L7) == s7 and GPIO.input(L8) == s8:
        return True
    else:
        return False

# Samma som ovan fast med sido LEDsen
def LED_side(s9, s10):    
    
    if GPIO.input(L9) == s9 and GPIO.input(L10) == s10:
        return True
    else:
        return False
# --------------------------------------------------------------------------------------
# Roterar till given riktning ----------------------------------- rotate
def rotate(Rotation, Current_Rotation):
    send_i2c_motor('2')
    #print('Rotating')
    print("Rotating from ",Current_Rotation, "to ", Rotation)

    # Bestämmer rotations håll -> Väntar tills alla främre IR har blivit vita -> Stannar när den känner av tejp på någon av mittersta 4 IR sensorer
    # Om den ska svänga 180 grader så loopar den 2 gånger alltså den gör 2st 90 graders svängar
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
            time.sleep(0.1)
            if find_tape and (LED_front(1, 1, 1, 0, 0, 1, 1, 1) or LED_front(1, 1, 0, 0, 1, 1, 1, 1) or LED_front(1, 1, 1, 1, 0, 0, 1, 1) or LED_front(1, 1, 1, 0, 1, 1, 1, 1) or LED_front(1, 1, 1, 1, 0, 1, 1, 1) or LED_front(1, 1, 1, 1, 1, 0, 1, 1) or LED_front(1, 1, 0, 1, 1, 1, 1, 1) or LED_front(1, 0, 1, 1, 1, 1, 1, 1) or LED_front(1, 1, 1, 1, 1, 1, 0, 1)):
                send_i2c_motor('S')
                time.sleep(0.5)
                Current_Rotation = Next_Rotation
            elif (LED_front(1,1,1,1,1,1,1,1) or LED_front(1,1,1,1,1,1,1,0) or LED_front(0,1,1,1,1,1,1,1) or LED_front(0,1,1,1,1,1,1,0) or LED_front(0,0,1,1,1,1,1,0) or LED_front(0,1,1,1,1,1,0,0) or LED_front(0,0,1,1,1,1,0,0) or LED_front(1,1,1,1,1,1,0,0) or LED_front(0,0,1,1,1,1,1,1) or LED_front(0,0,0,1,1,1,0,0) or LED_front(0,0,1,1,1,0,0,0) or LED_front(0,0,0,1,1,0,0,0)):
                find_tape = True
                time.sleep(0.1)

# ---------------------------------------------------------------- start_centering
def start_centering():
    send_i2c_motor('1')
    print("Trying to center")
    # Funktion för att centrera AGV på ett kors
    # (Fungerar ej , Ej testad)
    # Funktion:
    # (1) Backar tills den hittar en horisontell tejplinje -> (2) kör framåt tills någon av sido IRs känner av tejp ->
    # (3) roterar den sida som inte känt av en tejp tills båda sidor har känt av tejp -> (4) centrerar tejpen med främre IR
    send_i2c_motor('B') 
    tape_found = False
    find_last_A = False
    find_last_D = False
    while True:
        #(1)
        if not tape_found and (LED_front(0, 0, 0, 0, 0, 0, 0, 0) or LED_front(1, 0, 0, 0, 0, 0, 0, 0) or LED_front(0, 0, 0, 0, 0, 0, 0, 1) or LED_front(0,0,0,0,0,0,1,1) or LED_front(1,0,0,0,0,0,0,1) or LED_front(1,1,0,0,0,0,0,0) or LED_front(0,0,0,0,0,1,1,1) or LED_front(1,0,0,0,0,0,1,1) or LED_front(1,1,0,0,0,0,0,1) or LED_front(1,1,1,0,0,0,0,0) or LED_front(1,1,1,1,0,0,0,0) or LED_front(1,1,1,0,0,0,0,1) or LED_front(1,1,0,0,0,0,1,1) or LED_front(1,0,0,0,0,1,1,1) or LED_front(0,0,0,0,1,1,1,1)):
            send_i2c_motor('S')
            tape_found = True
            send_i2c_motor('F')
            time.sleep(0.2)
        # (2)
        elif tape_found and LED_side(1,0):
            send_i2c_motor('D')
            find_last_D = True
            tape_found = False
        elif tape_found and LED_side(0,1):
            send_i2c_motor('A')
            find_last_A = True
            tape_found = False
        elif tape_found and LED_side(0,0):
            send_i2c_motor('S')
            tape_found = False
            break
        # (3)
        elif (find_last_A and GPIO.input(L9)) or (find_last_D and GPIO.input(L10)):
            send_i2c_motor('S')
            break
            
    # (4)
    #find_center = False
    #start_drift = True
    while True:
        if (LED_front(1, 1, 1, 0, 0, 1, 1, 1) or LED_front(1, 1, 1, 0, 1, 1, 1, 1) or LED_front(1, 1, 1, 1, 0, 1, 1, 1)):
            send_i2c_motor('S')
            time.sleep(2)
            break
        elif (LED_front(1, 1, 1, 1, 0, 0, 1, 1) or LED_front(1, 1, 1, 0, 0, 0, 1, 1) or LED_front(1, 1, 1, 1, 1, 0, 0, 1) or LED_front(1, 1, 1, 1, 1, 0, 1, 1) or LED_front(1, 1, 1, 1, 1, 1, 0, 0) or LED_front(1, 1, 1, 1, 1, 1, 1, 0) or LED_front(1, 1, 1, 1, 1, 1, 0, 1)):
            send_i2c_motor('>')
        elif (LED_front(1, 1, 0, 0, 1, 1, 1, 1) or LED_front(1, 1, 0, 0, 0, 1, 1, 1) or LED_front(1, 0, 0, 1, 1, 1, 1, 1) or LED_front(1, 1, 0, 1, 1, 1, 1, 1) or LED_front(1, 0, 1, 1, 1, 1, 1, 1)  or LED_front(0, 1, 1, 1, 1, 1, 1, 1)or LED_front(0, 0, 1, 1, 1, 1, 1, 1)):
            send_i2c_motor('<')

def drive_centering():
    send_i2c_motor('1')
    time.sleep(0.1)
    send_i2c_motor('F')
    print("stopping at center")
    # Funktion för att centrera AGV på ett kors
    # (Fungerar ej , Ej testad)
    # Funktion:
    # (1) Backar tills den hittar en horisontell tejplinje -> (2) kör framåt tills någon av sido IRs känner av tejp ->
    # (3) roterar den sida som inte känt av en tejp tills båda sidor har känt av tejp -> (4) centrerar tejpen med främre IR
    find_last_A = False
    find_last_D = False
    while True:
        # (2)
        if LED_side(1,0):
            send_i2c_motor('D')
            find_last_D = True
        elif LED_side(0,1):
            send_i2c_motor('A')
            find_last_A = True
        elif LED_side(0,0):
            send_i2c_motor('S')
            break
        # (3)
        elif (find_last_A and GPIO.input(L9)) or (find_last_D and GPIO.input(L10)):
            send_i2c_motor('S')
            break
            
    # (4)
    #find_center = False
    #start_drift = True
    while True:
        if (LED_front(1, 1, 1, 0, 0, 1, 1, 1) or LED_front(1, 1, 1, 0, 1, 1, 1, 1) or LED_front(1, 1, 1, 1, 0, 1, 1, 1)):
            send_i2c_motor('S')
            print("centering done")
            time.sleep(1)
            break
        elif (LED_front(1, 1, 1, 1, 0, 0, 1, 1) or LED_front(1, 1, 1, 0, 0, 0, 1, 1) or LED_front(1, 1, 1, 1, 1, 0, 0, 1) or LED_front(1, 1, 1, 1, 1, 0, 1, 1) or LED_front(1, 1, 1, 1, 1, 1, 0, 0) or LED_front(1, 1, 1, 1, 1, 1, 1, 0) or LED_front(1, 1, 1, 1, 1, 1, 0, 1)):
            send_i2c_motor('>')
        elif (LED_front(1, 1, 0, 0, 1, 1, 1, 1) or LED_front(1, 1, 0, 0, 0, 1, 1, 1) or LED_front(1, 0, 0, 1, 1, 1, 1, 1) or LED_front(1, 1, 0, 1, 1, 1, 1, 1) or LED_front(1, 0, 1, 1, 1, 1, 1, 1)  or LED_front(0, 1, 1, 1, 1, 1, 1, 1)or LED_front(0, 0, 1, 1, 1, 1, 1, 1)):
            send_i2c_motor('<')
 
# ----------------------------------------------------------------- drive
# kör framåt och följerlinjen
def drive(current_pos_x, current_pos_y, next_x, next_y, x_dir, neg_dir):
    send_i2c_motor('3')
    # Funktion:
    # kör framåt och följerlinjen , Räknar varje kors, ändrar då på lokala nuvarande position
    #print("driving")
    find_tape = False
    while True:
        if (LED_front(1, 1, 1, 0, 0, 1, 1, 1) or LED_front(1, 1, 1, 1, 0, 1, 1, 1) or LED_front(1, 1, 1, 0, 1, 1, 1, 1)): #and distance1 > 5:
            send_i2c_motor('F')
        elif (LED_front(1, 1, 0, 0, 1, 1, 1, 1) or LED_front(1, 1, 0, 1, 1, 1, 1, 1) or LED_front(1, 0, 0, 1, 1, 1, 1, 1) or LED_front(1, 0, 1, 1, 1, 1, 1, 1) or LED_front(0, 0, 1, 1, 1, 1, 1, 1) or LED_front(0, 1, 1, 1, 1, 1, 1, 1) or LED_front(1,1,0,0,0,1,1,1) or LED_front(1,1,0,0,0,1,1,1)): #and distance1 > 5:
            send_i2c_motor('D')
        elif (LED_front(1, 1, 1, 1, 0, 0, 1, 1) or LED_front(1, 1, 1, 1, 1, 0, 1, 1) or LED_front(1, 1, 1, 1, 1, 0, 0, 1) or LED_front(1, 1, 1, 1, 1, 1, 0, 1) or LED_front(1, 1, 1, 1, 1, 1, 0, 0) or LED_front(1, 1, 1, 1, 1, 1, 1, 0) or LED_front(1,1,1,0,0,0,1,1)): #and distance1 > 5:
            send_i2c_motor('A')
        elif (LED_front(0, 0, 0, 0, 0, 0, 0, 0) or LED_front(1, 0, 0, 0, 0, 0, 0, 0) or LED_front(0, 0, 0, 0, 0, 0, 0, 1) or LED_front(0,0,0,0,0,0,1,1) or LED_front(1,0,0,0,0,0,0,1) or LED_front(1,1,0,0,0,0,0,0) or LED_front(0,0,0,0,0,1,1,1) or LED_front(1,0,0,0,0,0,1,1) or LED_front(1,1,0,0,0,0,0,1) or LED_front(1,1,1,0,0,0,0,0) or LED_front(1,1,1,1,0,0,0,0) or LED_front(1,1,1,0,0,0,0,1) or LED_front(1,1,0,0,0,0,1,1) or LED_front(1,0,0,0,0,1,1,1) or LED_front(0,0,0,0,1,1,1,1)):# or LED_front(0,0,0,1,1,1,1,1) or LED_front(1,1,1,1,1,0,0,0)):# or LED_front(1,1,1,1,1,0,0,0) or LED_front(0,0,0,1,1,1,1,1)): #  or LED_front(1,1,1,1,0,0,0,1) or LED_front(1,1,1,0,0,0,1,1) or LED_front(1,1,0,0,0,1,1,1) or LED_front(1,0,0,0,1,1,1,1)): and distance1 > 5:
            send_i2c_motor('F')
            time.sleep(0.2)
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
        else:
            send_i2c_motor('F')
        
        #elif next_x != current_pos_x or next_y != current_pos_y:
            #if sensor_process_1() < 2:
                #status = False
                #send_i2c_motor('S')
    
    if next_x == current_pos_x and next_y == current_pos_y:
        print("center check: ",next_x, current_pos_x, next_y, current_pos_y)
        drive_centering()
    print("At : ",current_pos_x,current_pos_y)
    return current_pos_x, current_pos_y


# -------------------------------------------------------------------- picking

# Implementera max tid

def picking(PickPosition, Current_Rotation):
    send_i2c_motor('1')
    # Funktion: (Samma för alla riktningar)
    # (1) Roterar mot plock lådan -> (2) mäter nuvarande avståndet till lådan -> (3) kör fram tills den är ungefär 4cm från lådan ->
    # (4) Blinkar lampan -> (5) Läser av med kameran (Ej implementerat) -> (6) Backar till den avlästa distansen i början
    print("Picking", PickPosition)
    if PickPosition == 'PN':
        rotate('N', Current_Rotation) # (1)
        start_centering()
        time.sleep(2)
        start_dist = sensor_process_1() # (2) Spara original distansen till kuben
        print("Start Distance: ", start_dist)
        if start_dist > 20:
            start_dist = 20
        timer = time.time() 
        dist = sensor_process_1()
        print("dist:",dist)
        send_i2c_motor('2')
        while dist > 3 and time.time() - timer < 0.5:# Kör fram till vi är nära kuben
            dist = sensor_process_1()
            #print("dist:",dist)
            send_i2c_motor('F')
        send_i2c_motor('S')
        #Blinka LEDs och vänta
        #LED_light(True) # (4)
        print(LED_detect()) # (5)
        #LED_light(False)
        start_centering()
        """while sensor_process_1() < start_dist-3: # Backa tills vi är på original distansen
            send_i2c_motor('B')
        send_i2c_motor('S')""" 
        
    elif PickPosition == 'PS':   
        rotate('S', Current_Rotation)
        start_centering()
        time.sleep(2)
        start_dist = sensor_process_1() # Spara original distansen till kuben
        print("Start Distance: ", start_dist)
        if start_dist > 20:
            start_dist = 20
        timer = time.time()
        dist = sensor_process_1()
        print("dist:",dist)
        send_i2c_motor('2')
        while dist > 3 and time.time() - timer < 0.5:# Kör fram till vi är nära kuben
            dist = sensor_process_1()
            #print("dist:",dist)
            send_i2c_motor('F')
        send_i2c_motor('S')
        #Blinka LEDs och vänta
        #LED_light(True) # (4)
        print(LED_detect()) # (5)
        #LED_light(False)
        start_centering()
        """while sensor_process_1() < start_dist-3: # Backa tills vi är på original distansen
            send_i2c_motor('B')
        send_i2c_motor('S')"""

    elif PickPosition == 'PW':
        rotate('W', Current_Rotation)
        start_centering()
        time.sleep(2)
        start_dist = sensor_process_1() # Spara original distansen till kuben
        print("Start Distance: ", start_dist)
        if start_dist > 20:
            start_dist = 20
        timer = time.time()
        dist = sensor_process_1()
        print("dist:",dist)
        send_i2c_motor('2')
        while dist > 3 and time.time() - timer < 0.5:# Kör fram till vi är nära kuben
            dist = sensor_process_1()
            #print("dist:",dist)
            send_i2c_motor('F')
        send_i2c_motor('S')
        #Blinka LEDs och vänta
        #LED_light(True) # (4)
        print(LED_detect()) # (5)
        #LED_light(False)
        start_centering()
        """while sensor_process_1() < start_dist-3: # Backa tills vi är på original distansen
            send_i2c_motor('B')
        send_i2c_motor('S')"""

    elif PickPosition == 'PE': 
        rotate('E', Current_Rotation)
        start_centering()
        time.sleep(2)
        start_dist = sensor_process_1() # Spara original distansen till kuben
        print("Start Distance: ", start_dist)
        if start_dist > 20:
            start_dist = 20
        timer = time.time()
        dist = sensor_process_1()
        print("dist:",dist)
        send_i2c_motor('2')
        while dist > 3 and time.time() - timer < 0.5:# Kör fram till vi är nära kuben
            dist = sensor_process_1()
            #print("dist:",dist)
            send_i2c_motor('F')
        send_i2c_motor('S')
        #Blinka LEDs och vänta
        #LED_light(True) # (4)
        print(LED_detect()) # (5)
        #LED_light(False)
        start_centering()
        """while sensor_process_1() < start_dist-3: # Backa tills vi är på original distansen
            send_i2c_motor('B')
        send_i2c_motor('S')"""
        

def stop():
    send_i2c_motor('S')
