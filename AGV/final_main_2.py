import bluetooth 
from navigation2 import AutonomousVehicle 
from multiprocessing import Process, Value 
import time 
import threading 
import select 
from datetime import datetime
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ina260
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Init currentsensor and display
# Constants

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 32
# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Initialize INA260
ina260 = adafruit_ina260.INA260(i2c)
# Initialize SSD1306 OLED display
disp = adafruit_ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)
# Clear display
disp.fill(0)
disp.show()
# Create blank image for drawing
width = disp.width
height = disp.height
image = Image.new("1", (width, height))
# Initialize drawing object
draw = ImageDraw.Draw(image)
draw.font = ImageFont.load_default()



def update_power():
    while True:
        # Clear display
        disp.fill(0)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Read sensor data
        current_mA = ina260.current
        voltage_V = ina260.voltage
        power_mW = ina260.power

        # Display data on OLED
        draw.text((0, 0), f"Current: {current_mA:.2f} mA", font=draw.font, fill=255)
        draw.text((0, 10), f"Voltage: {voltage_V:.2f} V", font=draw.font, fill=255)
        draw.text((0, 20), f"Power: {power_mW:.2f} mW", font=draw.font, fill=255)

        # Display image
        disp.image(image)
        disp.show()
        time.sleep(0.5)

def send_updates(client_sock, status, vehicle, stop_send):
    global stop_threads
    while True:
        # Ta fram nuvarande tiden i rätt format
        now = datetime.now() 
        current_time = now.strftime("%H:%M:%S")
        
        # Tar fram status och koordinater från AGVn (Fungerar ej, Troligen för att koordinaterna ändras i en process vilket gör att de inte uppdateras här) 
        coordinates = vehicle.get_coordinates()
        status = vehicle.get_AGV_status()
        
        #Skapa strängen som ska skickas till ÖS
        update = f"{current_time}_{coordinates}_{status}\n"
        
        # stop_threads ska ändras när man tar emot ett S frän ÖS (Ej testat)
        if stop_send():
            print("Paused send thread")
            while stop_send():
                time.sleep(2)
            print("Resuming send thread")
            
        
        # Prova att skicka uppdatering till ÖS annars skriv ett error meddelande och avbryt loopen
        try: 
            client_sock.send(update.encode('utf-8')) 
        except Exception as e: 
            print(f"Error in send_updates: {e}") 
            break 
        time.sleep(2)

def RXTX_messages(client_sock, status, send_thread, stop_threads, vehicle): 
    status = 'I'
    vehicle.set_AGV_status(status)
    while True:
        
        #Läs från bluetooth bufferten och kör kod beroende på mottagen bokstav
        try: 
            ready_to_read, _, _ = select.select([client_sock], [], [], 0.1) 
            data = client_sock.recv(1024) 
            decoded_data = data.decode('utf-8') 
            print(f"Received: {decoded_data}") 
            if decoded_data[9] == 'S':
                vehicle.set_status(False) # stoppa navigeringen!
                stop_threads = True
                now = datetime.now() 
                current_time = now.strftime("%H:%M:%S")
                update = f"{current_time}_{vehicle.get_coordinates()}_{status}\n" 
                client_sock.send(update.encode('utf-8'))
            elif decoded_data[9] == 'C': 
                now = datetime.now() 
                current_time = now.strftime("%H:%M:%S")
                update = f"{current_time}_{vehicle.get_coordinates()}_{status}\n" 
                client_sock.send(update.encode('utf-8')) 
            elif decoded_data[9] == 'B':# or vehicle.status.value == 'W':
                stop_threads = False
                if send_thread is None or send_thread.is_alive() == False: 
                    send_thread = threading.Thread(target=send_updates, args=(client_sock, status, vehicle, (lambda : stop_threads))) 
                    send_thread.start()
                vehicle.set_status(True) # starta navigeringen!
                  
            elif str(data[10]).isdigit(): # Om vi tar emot en siffra så är det en rutt
                now = datetime.now() 
                current_time = now.strftime("%H:%M:%S") 
                route_plan = get_route_plan(decoded_data) 
                copy_route = f"{current_time}_{route_plan}\n" 
                vehicle.set_route_plan(route_plan) 
                client_sock.send(copy_route.encode('utf-8'))
            
        except Exception as e: 
            print(f"Error in receive_messages: {e}") 
            break
    send_thread.join()
# Skickar tillbaka ruttplanen
def get_route_plan(data): 
    route_plan = data[9:] 
    start_pos = route_plan[10:20] 
    return route_plan


# MAIN ------------------------------------------------------ MAIN
# Skapa ett objekt av klassen AutonomousVehicle 
vehicle = AutonomousVehicle()
stop_threads = False # Används för att stänga alla trådar
status = ''
send_thread = None 

while True:
    #Skapa bluetooth förbindelse
    try:
        powersensor_thread = threading.Thread(target=update_power, args=())
        powersensor_thread.start()
        print(f"Searching bluetooth connection...")
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM) 
        server_sock.bind(("", bluetooth.PORT_ANY)) 
        server_sock.listen(1) 
        client_sock, client_info = server_sock.accept() 
        print(f"Accepted connection from {client_info}")
        #RXTX_messages(client_sock, status, send_thread, stop_threads, vehicle)
        receive_thread = threading.Thread(target=RXTX_messages, args=(client_sock, status, send_thread, stop_threads, vehicle)) 
        receive_thread.start()  
    except IOError as e: 
        print(f"Connection lost: {e}, trying to reconnect...") 
        continue 
    finally: # När rutten avslutas så stängs förbindelsen
        receive_thread.join()
        print("Ending Program")
        stop_threads = True
        if client_sock: 
            client_sock.close() 
        if server_sock: 
            server_sock.close()
        GPIO.cleanup()
        break
    
    #10:59:12.077_180060_PW_330060_330000_420000_PN_450000_450150_510150_PS_510210_570210_PE_360210_360180__360150_180150_180090_000090_D_F
 
