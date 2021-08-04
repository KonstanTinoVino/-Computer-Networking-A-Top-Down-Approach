from socket import *

server_address = ('localhost', 12000)
clientSocket = socket(AF_INET, SOCK_DGRAM)
client_address = ('localhost', 1231)
clientSocket.bind(client_address)
message = input("Input lowercase sentence")
print("Recieved input: " + message)
clientSocket.sendto(message.encode(),server_address)
modifiedMessage, serverAddress = clientSocket.recvfrom(1201)
print(modifiedMessage.decode())
clientSocket.close()