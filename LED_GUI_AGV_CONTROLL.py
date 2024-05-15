import tkinter as tk
import RPi.GPIO as GPIO
from smbus import SMBus
import time
#import IR_LED_GUI
GPIO.setmode(GPIO.BCM)
# --------------------------------I2C------------------------------------
addr = 0x8  # bus address arduino
BUS = 1

bus = SMBus(BUS)  # indicates /dev/ic2-1
time.sleep(1)



# left leds
led_pins = [26, 19, 13, 6, 5, 11, 9, 10, 17, 27]
for pin in led_pins:
    GPIO.setup(pin, GPIO.IN)

# Skapa ett fönster med Tkinter
root = tk.Tk()
root.title("LED Status")

# Skapa en ram för att placera rutorna
frame = tk.Frame(root)
frame.pack()



# Funktion för att uppdatera rutorna baserat på LED-status
def update_leds():
    led_states = [GPIO.input(pin) for pin in led_pins]
    for i, led_state in enumerate(led_states):
        if led_state:
            led_labels[i].config(bg="white")
        else:
            led_labels[i].config(bg="black")
    root.after(100, update_leds)  # Uppdatera var 100 ms
    
def key_down(event):
    #print(event.keysym, event.keycode)
    if event.keycode == 113:
        send_i2c_motor('L')
    elif event.keycode == 114:
        send_i2c_motor('R')
    elif event.keycode == 111:
        send_i2c_motor('F')
    elif event.keycode == 116:
        send_i2c_motor('B')
    elif event.keycode == 38:
        send_i2c_motor('>')
    elif event.keycode == 40:
        send_i2c_motor('<')

def key_up(event):
    #print(event.keysym, event.keycode)
    if event.keycode == 113:
        send_i2c_motor('S')
    elif event.keycode == 114:
        send_i2c_motor('S')
    elif event.keycode == 111:
        send_i2c_motor('S')
    elif event.keycode == 116:
        send_i2c_motor('S')
    elif event.keycode == 38:
        send_i2c_motor('S')
    elif event.keycode == 40:
        send_i2c_motor('S')


# Skickar kommandon till Arduino
def send_i2c_motor(cmd):
    bus.write_byte_data(addr, 0, ord(cmd[0]))
    # En viss delay behövs just nu för att vi inte ska fä en I2C krash ibland, när data skickas för fort
    # Dock så ger en högre delay ojämnare körning hos AGVn. Detta behöver lösas och har ganksa hög PRIO
    time.sleep(0.01) 
    #print(f"Sent {cmd} to Arduino")

send_i2c_motor('5')

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

# Skapa etiketter för varje LED
led_labels = []
for i in range(8):
    label = tk.Label(frame, text=f"LED {i+1}", width=10, height=2, bg="white")
    label.grid(row=0, column=i, padx=5, pady=5)
    led_labels.append(label)
label = tk.Label(frame, text=f"LED {9}", width=10, height=2, bg="white")
label.grid(row=1, column=0, padx=5, pady=5)
led_labels.append(label)
label = tk.Label(frame, text=f"LED {10}", width=10, height=2, bg="white")
label.grid(row=1, column=7, padx=5, pady=5)
led_labels.append(label)

# Starta funktionen för att uppdatera rutorna
update_leds()

# Avsluta GUI: en när fönstret stängs
root.protocol("WM_DELETE_WINDOW", root.quit)

# Visa fönstret
root.mainloop()

# Stäng ner GPIO-portarna när programmet avslutas
GPIO.cleanup()

