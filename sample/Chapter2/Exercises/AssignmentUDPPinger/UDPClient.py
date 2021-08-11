from socket import *
import time

# Creating Object Addresses
server_address = ('localhost', 12000)
client_address = ('localhost', 1231)

# Creating client socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(client_address)
clientSocket.settimeout(1)

# Send 10 requests to UDP server
for i in 10:
    message = "message: " + i

    start_time = time.time()
    clientSocket.sendto(message.encode(), server_address)
    modifiedMessage, serverAddress = clientSocket.recvfrom(1201)
    end_time = time.time()

    print(modifiedMessage.decode())
    clientSocket.close()
