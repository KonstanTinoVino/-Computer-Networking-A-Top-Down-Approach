from socket import *
import requests
r =requests.get('https://xkcd.com/1906/')
server_address = ('localhost', 12000)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(server_address)
sentence = "GET /somedir/ducks.png HTTP/1.1" + "\r\n" + "Host: www.someschool.edu" + "\r\n" +"Connection: close" \
           + "\r\n" + "User-agent: Mozilla/5.0" + "\r\n" +"Accept-language: fr "
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print("From Server:", modifiedSentence.decode())
filedata = clientSocket.recv(167642)
print(filedata)
clientSocket.close()