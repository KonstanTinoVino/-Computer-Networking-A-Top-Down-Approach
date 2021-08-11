from socket import *
from datetime import datetime


RTT_times = []

# Creating Object Addresses
server_address = ('localhost', 12000)
client_address = ('localhost', 1071)

# Creating client socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(client_address)
clientSocket.settimeout(1)

# Send 10 requests to UDP server
for i in range(10):
    message = "message: " + str(i)

    start_time = datetime.now()
    clientSocket.sendto(message.encode(), server_address)
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        end_time = datetime.now()
        RTT = end_time - start_time
        print("Ping " + modifiedMessage.decode() + " " + str(RTT))
    except:
        print("Request timed out")