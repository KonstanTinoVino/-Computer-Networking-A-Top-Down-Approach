from socket import *


class Server:

    def __init__(self, ip_address, port_number, server_socket, listener):
        self.ip_address = ip_address
        self.port_number = port_number
        self.socket = self.map_socket(server_socket)
        self.socket.bind((ip_address, port_number))
        self.socket.listen(listener)

    def map_socket(self, server_socket):
        if server_socket == "TCP":
            self.socket = socket(AF_INET,SOCK_STREAM)
        elif server_socket == "UDP":
            self.socket = socket(AF_INET, SOCK_DGRAM)
        return self.socket
