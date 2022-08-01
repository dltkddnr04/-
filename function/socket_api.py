from socket import *
import json

class socket_communication():
    def __init__():
        return

    def server_setup(port_number):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(('', port_number))
        server_socket.listen(1)

    def client_setup(ip_address, port_number):
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((ip_address, port_number))

    def receive_data(socket, size):
        receive_data = socket.recv(size)
        receive_data = receive_data.decode('utf-8')
        return receive_data
    
    def send_data(socket, data):
        socket.send(data.encode('utf-8'))