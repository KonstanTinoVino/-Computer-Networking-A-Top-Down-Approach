from socket import *
import time
from pathlib import Path
import io
import sys

duckFile = Path('D:/Work/Exercise/Resources/duck.png')
filename = "duck.png"


def getfilerequest(requestmessage):
    try:
        heather, rest = requestmessage.split("\r\n", 1)
        method, url, version = heather.split(" ", 2)
        return url
    except:
        print("Unexpected error:", sys.exc_info()[0])

def constructresponseheather(duck):
    ts = time.gmtime()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    if duck is True:
        return "HTTP/1.1 200 OK" + "\r\n" + "Connection: close" + "\r\n" + "Date: " + timestamp + "\r\n" + "Server: TinoServer" + "\r\n" + "Last-Modified: Tue, 18 Aug 2015 15:11:03 GMT" + "\r\n"
    else:
        return "HTTP/1.1 404 Not Found"+ "\r\n" + "Connection: close" + "\r\n" + "Date: " + timestamp + "\r\n" + "Server: TinoServer" + "\r\n"


def constructresponse(duck):
    if duck is not True:
        return constructresponseheather(duck)
    else:
        heather = constructresponseheather(duck)
        heather += "Content-Length: " + str(duckFile.stat().st_size) + "\r\n"
        heather += "Content-Type: image/png" + "\r\n"
        heather += "\r\n"
        return heather


server_address = ('localhost', 12000)
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(server_address)
serverSocket.listen(5)
print("The server is ready to receive")
while True:
    connectionSocket, addr = serverSocket.accept()
    response = connectionSocket.recv(1024).decode()
    url = getfilerequest(response)
    if url is not None:
        filerequesst = url.split('/')[-1]
        if filerequesst == "duck.png":
            response =constructresponse(True)
        else:
            response = constructresponse(False)
        print(response)
        connectionSocket.send(response.encode())
        bytes_read = open(duckFile, encoding="utf8", errors="ignore").read()
        connectionSocket.sendall(bytes_read.encode())


    connectionSocket.close()

