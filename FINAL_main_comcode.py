import bluetooth
#import cam_led_detection
#import send_i2c_motor
#import ultrasonic
import time
from multiprocessing import Process, Value
import threading
import select
from datetime import datetime

# Skapa delade minnesplatser för att lagra avstånden
distance1 = Value('i', 0)
distance2 = Value('i', 0)

# Starta sensor-processerna
#Process(target=ultrasonic.sensor_process_1, args=(distance1,)).start()
#Process(target=ultrasonic.sensor_process_2, args=(distance2,)).start()

def send_updates(client_sock, status):
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S:%f")[:-3]
        # Konvertera distance1 och distance2 till heltal innan du skriver ut dem
        update = f"{current_time}_xxxyyy_{status[0]}\n"
        print(f'Sending {current_time}_xxxyyy_{status[0]}')
        

        
        try:
            client_sock.send(update.encode('utf-8'))
            if status[0] == 'I':
                if send_thread[0].is_alive():
                    return
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
            
            if decoded_data[13] == 'S':
                status[0] = 'I'
                print("Stopping")
                
            elif decoded_data[13] == 'C':
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S:%f")[:-3]
                update = f"{current_time}_xxxyyy_{status[0]}\n"
                client_sock.send(update.encode('utf-8'))
                print("Sending status once")
            
            elif decoded_data[13] == 'B':
                status[0] = 'W'
                print("Sending status continualy")
                if send_thread[0] is None or not send_thread[0].is_alive():
                    send_thread[0] = threading.Thread(target=send_updates, args=(client_sock, status))
                    send_thread[0].start()
            
            elif str(data[14]).isdigit(): # Reciveing route
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S:%f")[:-3]
                route_plan = get_route_plan(decoded_data)
                copy_route = f"{current_time}_{route_plan}\n"
                client_sock.send(copy_route.encode('utf-8'))
                #print('Route received: {route_plan}')

        except Exception as e:
            print(f"Error in receive_messages: {e}")
            continue

def get_route_plan(data):
    route_plan = data[13:]
    start_pos = route_plan[14:20]
    return route_plan
#def conect()
 #       server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
  #      server_sock.bind(("", bluetooth.PORT_ANY))
   #     server_sock.listen(1)

    #    client_sock, client_info = server_sock.accept()
     #   print(f"Accepted connection from {client_info}")

      #  receive_thread = threading.Thread(target=RXTX_messages, args=(client_sock, status, send_thread))
       # receive_thread.start()

        #receive_thread.join()
    


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
        break
