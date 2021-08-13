from socket import *
import tempfile
from pathlib import Path
import os


def get_file_path(file):
    dirname = os.path.dirname(__file__)
    return Path(os.path.join(dirname, 'Resources/' + file))


# Create a server socket, bind it to a port and start listening
server_address = ("localhost", 8888)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(server_address)
tcpSerSock.listen(1)

while True:
    # Strat receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(8888).decode()
    print("Message Output-------------------------")
    print(message)
    print("Message End-------------------------")

    # Extract the filename from the given message
    print(message.split()[1])
    act_host = message.split()[1]
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = "false"
    filetouse = get_file_path(filename)
    print(filetouse)
    try:
        # Check wether the file exist in the cache
        check = filename.replace("www.","",1).split(".", 1)[0]
        f = open(get_file_path(check+".html"), "rb")
        outputdata = f.readlines()
        fileExist = "true"
        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.1 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())
        for data in outputdata:
            tcpCliSock.sendall(data)
        print('Read from cache')
    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            proxy_address = ("localhost", 80)
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.","",1)
            prefix = hostn.split(".", 1)[0]
            print(hostn)

            # Connect to the socket to port 80
            new_mes = message.replace(act_host, hostn).replace("localhost:8888", filename)
            print("meess----------")
            print(new_mes)
            print("meess----------")
            c.connect((hostn, 80))
            c.send(new_mes.encode())
            returned_message = c.recv(8000)
            print("meess----------")
            print(returned_message)
            # Create a temporary file on this socket and ask port 80 for the file requested by the client
            f = open( get_file_path(prefix + ".html"), "x")
            f.write(returned_message.decode())
            f.close()
            # Read the response into buffer
            # Create a new file in the cache for the requested file.
            # Also send the response in the buffer to client socket and the corresponding file in the cache
            tcpCliSock.send(returned_message)

        else:
            # HTTP response message for file not found
            tcpCliSock.send("HTTP/1.1 404 Not Found\r\n")
            tcpCliSock.send("\r\n")
            tcpCliSock.send("\r\n")
    # Close the client and the server sockets
    tcpCliSock.close()
tcpSerSock.close()