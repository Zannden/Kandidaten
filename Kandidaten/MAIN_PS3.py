import bluetooth
from smbus import SMBus
import RPi.GPIO as GPIO
import time
from evdev import InputDevice, categorize, ecodes
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)



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


gamepad = InputDevice('/dev/input/event1')
print(gamepad)

# PS3 buttoncodes
Xbtn = 304
Obtn = 305
Tbtn = 307
Sbtn = 308
Hpil = 547
Vpil = 546
Upil = 544
Npil = 545
R1 = 311
R2 = 313
L1 = 310
L2 = 312

addr = 0x8  # bus address arduino
BUS = 1


bus = SMBus(BUS)  # indicates /dev/ic2-1
time.sleep(1);
# --------------------------------------------------------------------- I2C
def send_command(cmd):
    bus.write_byte_data(addr, 0, ord(cmd[0]))
    print(f"Sent {cmd} to Arduino")

# --------------------------------------------------------------------- LED class id and state
class LED:
    def __init__(self, ID, state):
        self.ID = ID;
        self.state = state;
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
    print(GPIO.input(L1),GPIO.input(L2),GPIO.input(L3),GPIO.input(L4),GPIO.input(L5),GPIO.input(L6),GPIO.input(L7),GPIO.input(L8))
    if GPIO.input(L1)==s1 and GPIO.input(L2)==s2 and GPIO.input(L3)==s3 and GPIO.input(L4)==s4 and GPIO.input(L5)==s5 and GPIO.input(L6)==s6 and GPIO.input(L7)==s7 and GPIO.input(L8)==s8:
        return True
    else:
        return False;
    


# --------------------------------------------------------------------- IR



# --------------------------------------------------------------------- PS3
drive_F = False
for event in gamepad.read_loop():
    #filter by event type
    if event.type == ecodes.EV_KEY:
        if event.value == 1:
            if event.code == Upil :
                drive_F = True
                print("^")
        elif event.value == 0:
            if event.code == Upil :
                drive_F = False
                print("stop")
    #print("loop")    
    if drive_F and (LED_state(1,1,1,0,0,1,1,1) or LED_state(1,1,1,1,0,1,1,1) or LED_state(1,1,1,0,1,1,1,1)):
        #send_command("F")
        print("F")
    elif drive_F and (LED_state(1,1,0,0,1,1,1,1) or LED_state(1,1,0,1,1,1,1,1)):
        #send_command("R")
        print("L")
    elif drive_F and (LED_state(1,1,1,1,0,0,1,1) or LED_state(1,1,1,1,1,0,1,1)):
        #send_command("L")
        print("R")
        
        
    if not drive_F:
        None
        #send_command("S")
        #print("Drive_stop")
            


        



