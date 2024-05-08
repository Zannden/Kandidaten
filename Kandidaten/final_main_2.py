import bluetooth 
from navigation2 import AutonomousVehicle 
from multiprocessing import Process, Value 
import time 
import threading 
import select 
from datetime import datetime 

# Skapa ett objekt av klassen AutonomousVehicle 
vehicle = AutonomousVehicle()

def send_updates(client_sock, vehicle.get_AGV_status(),vehicle.get_AGV_status()): 
    while True: 
        now = datetime.now() 
        current_time = now.strftime("%H:%M:%S")
        # Använd get_coordinates-metoden från AutonomousVehicle 
        #coordinates = vehicle.get_coordinates(10, 20) 
        update = f"{current_time}_{vehicle.get_AGV_status()}_{vehicle.get_AGV_status()}\n" 
        try: 
            client_sock.send(update.encode('utf-8')) 
        except Exception as e: 
            print(f"Error in send_updates: {e}") 
            break 
        time.sleep(2)

def RXTX_messages(client_sock, status, send_thread): 
    status[0] = 'I' 
    while True: 
        try: 
            ready_to_read, _, _ = select.select([client_sock], [], [], 0.1) 
            data = client_sock.recv(1024) 
            decoded_data = data.decode('utf-8') 
            print(f"Received: {decoded_data}") 
            if decoded_data[9] == 'S': 
                vehicle.set_status(False) # stoppa navigeringen!  
            elif decoded_data[9] == 'C': 
                now = datetime.now() 
                current_time = now.strftime("%H:%M:%S")
                update = f"{current_time}_{vehicle.get_coordinates()}_{status[0]}\n" 
                client_sock.send(update.encode('utf-8')) 
            elif decoded_data[9] == 'B':# or vehicle.status.value == 'W': 
                vehicle.set_status(True) # starta navigeringen! 
                if send_thread[0] is None or not send_thread[0].is_alive(): 
                send_thread[0] = threading.Thread(target=send_updates, args=(client_sock, vehicle.get_AGV_status(), vehicle.get_AGV_status()) 
                    send_thread[0].start()  
            elif str(data[10]).isdigit(): 
                now = datetime.now() 
                current_time = now.strftime("%H:%M:%S") 
                route_plan = get_route_plan(decoded_data) 
                copy_route = f"{current_time}_{route_plan}\n" 
                vehicle.set_route_plan(route_plan) 
                client_sock.send(copy_route.encode('utf-8')) 
        except Exception as e: 
            print(f"Error in receive_messages: {e}") 
            break 

def get_route_plan(data): 
    route_plan = data[9:] 
    start_pos = route_plan[10:20] 
    return route_plan 

status = [''] 
send_thread = [None] 

while True: 
    try: 
        server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM) 
        server_sock.bind(("", bluetooth.PORT_ANY)) 
        server_sock.listen(1) 
        client_sock, client_info = server_sock.accept() 
        print(f"Accepted connection from {client_info}") 
        receive_thread = threading.Thread(target=RXTX_messages, args=(client_sock, status, send_thread)) 
        receive_thread.start() 
        receive_thread.join() 
    except IOError as e: 
        print(f"Connection lost: {e}, trying to reconnect...") 
        continue 
    finally: 
        if client_sock: 
            client_sock.close() 
        if server_sock: 
            server_sock.close()
        #GPIO.cleanup()
        break
    
    #10:59:12.077_180060_PW_330060_330000_420000_PN_450000_450150_510150_PS_510210_570210_PE_360210_360180__360150_180150_180090_000090_D_F
