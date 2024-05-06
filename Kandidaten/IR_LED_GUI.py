import tkinter as tk
import RPi.GPIO as GPIO

# Konfigurera GPIO-pinnarna för att läsa LED-status
GPIO.setmode(GPIO.BCM)

# left leds
led_pins = [26, 19, 13, 6, 5, 11, 9, 10]
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

# Skapa etiketter för varje LED
led_labels = []
for i in range(8):
    label = tk.Label(frame, text=f"LED {i+1}", width=10, height=2, bg="white")
    label.grid(row=0, column=i, padx=5, pady=5)
    led_labels.append(label)

# Starta funktionen för att uppdatera rutorna
update_leds()

# Avsluta GUI: en när fönstret stängs
root.protocol("WM_DELETE_WINDOW", root.quit)

# Visa fönstret
root.mainloop()

# Stäng ner GPIO-portarna när programmet avslutas
GPIO.cleanup()

