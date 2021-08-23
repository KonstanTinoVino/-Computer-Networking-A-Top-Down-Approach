from socket import *
server_address = ('localhost', 12000)
client_address = ('localhost', 1231)
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(server_address)
print("The server is ready to receive")
while True:
    message, clientAddress = sock.recvfrom(1201)
    modifiedMessage = message.decode().upper()
    sock.sendto(modifiedMessage.encode(),client_address)