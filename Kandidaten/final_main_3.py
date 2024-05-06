import bluetooth
from multiprocessing import Process, Manager
from datetime import datetime
import threading
import time
from navigation2 import AutonomousVehicle

class BluetoothServer:
    def __init__(self):
        self.vehicle = AutonomousVehicle()
        self.status = Manager().Value(str, '')  # Delad variabel för status
        self.send_thread = Manager().list([None])  # Delad variabel för sändtråd

    def send_updates(self, client_sock):
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S:%f")[:-3]
            update = f"{current_time}_{self.vehicle.get_coordinates()}_{self.vehicle.get_AGV_status()}\n"
            try:
                client_sock.send(update.encode('utf-8'))
            except Exception as e:
                print(f"Error in send_updates: {e}")
                break
            time.sleep(2)

    def receive_messages(self, client_sock):
        self.status.value = 'I'
        while True:
            try:
                data = client_sock.recv(1024)
                decoded_data = data.decode('utf-8')
                print(f"Received: {decoded_data}")
                if decoded_data[13] == 'S':
                    self.vehicle.set_status(False)  # Stop navigation!
                elif decoded_data[13] == 'C':
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S:%f")[:-3]
                    update = f"{current_time}_{self.vehicle.get_coordinates()}_{self.status[0]}\n"
                    client_sock.send(update.encode('utf-8'))
                elif decoded_data[13] == 'B':
                    self.vehicle.set_status(True)  # Start navigation!
                    if self.send_thread[0] is None or not self.send_thread[0].is_alive():
                        self.send_thread[0] = threading.Thread(target=self.send_updates, args=(client_sock,))
                        self.send_thread[0].start()
                elif self.vehicle.status.value == 'X':
                    self.status[0] = 'X'
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S:%f")[:-3]
                    update = f"{current_time}_{self.vehicle.get_coordinates()}_{self.status[0]}\n"
                    client_sock.send(update.encode('utf-8'))
                elif str(data[14]).isdigit():
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S:%f")[:-3]
                    route_plan = self.get_route_plan(decoded_data)
                    copy_route = f"{current_time}_{route_plan}_{self.status[0]}\n"
                    self.vehicle.set_route_plan(route_plan)
                    client_sock.send(copy_route.encode('utf-8'))
            except Exception as e:
                print(f"Error in receive_messages: {e}")
                break

    def get_route_plan(self, data):
        route_plan = data[13:]
        start_pos = route_plan[14:20]
        return route_plan

def start_bluetooth_server():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)
    client_sock, client_info = server_sock.accept()
    print(f"Accepted connection from {client_info}")

    bluetooth_server = BluetoothServer()
    send_thread = threading.Thread(target=bluetooth_server.send_updates, args=(client_sock,))
    receive_thread = threading.Thread(target=bluetooth_server.receive_messages, args=(client_sock,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    client_sock.close()
    server_sock.close()
