from socket import *
from datetime import datetime
import time


RTT_times = []
lost = 0

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

    start_time = time.perf_counter()
    clientSocket.sendto(message.encode(), server_address)
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        end_time = time.perf_counter()
        RTT = end_time - start_time
        RTT_times.append(RTT)
        print("Ping " + modifiedMessage.decode() + " " + str(RTT))
    except:
        lost += 1
        print("Request timed out")

print("\n")
print("Maximum RTT = " + str(max(RTT_times)))
print("Minimum RTT = " + str(min(RTT_times)))
print("Average RTT = " + str(sum(RTT_times)/float(len(RTT_times))))
print("Packet Loss Percentage = " + str(float(lost)/10 * 100))