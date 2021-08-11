import os
import sys
import time
from pathlib import Path
from sample.Chapter2.Exercises.server import Server
from threading import Thread

dirname = os.path.dirname(__file__)
duckFile = Path(os.path.join(dirname, 'Resources/duck.png'))
filename = "duck.png"
server_socket = Server("localhost", 12000, "TCP", 1)


def get_file_request(request_message):
    try:
        heather, rest = request_message.split("\r\n", 1)
        method, url, version = heather.split(" ", 2)
        return url
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return ""


def return_file(file):
    return Path(os.path.join(dirname, 'Resources/' + file))


def check_if_file_exists(file):
    return os.path.exists(os.path.join(dirname, 'Resources/' + file))


def construct_response_heather(duck):
    ts = time.gmtime()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    if duck is True:
        return "HTTP/1.1 200 OK" + "\r\n" + "Connection: close" + "\r\n" + "Date: " + timestamp + "\r\n" + \
               "Server: TinoServer" + "\r\n" + "Last-Modified: Tue, 18 Aug 2015 15:11:03 GMT" + "\r\n"
    else:
        return "HTTP/1.1 404 Not Found"+ "\r\n" + "Connection: close" + "\r\n" + "Date: " + timestamp + "\r\n" + "Server: TinoServer" + "\r\n"


def construct_response(duck):
    if duck is not True:
        return construct_response_heather(duck)
    else:
        heather = construct_response_heather(duck)
        heather += "Content-Length: " + str(duckFile.stat().st_size) + "\r\n"
        heather += "Content-Type: image/png" + "\r\n"
        heather += "\r\n"
        return heather


def server_thread(port, thread):
    print("The server is ready to receive")
    while True:
        connection_socket, addr = server_socket.socket.accept()
        response = connection_socket.recv(port).decode()
        url = get_file_request(response)
        if url is not None:
            print("received request for Thread" + thread)
            file_request = url.split('/')[-1]
            exists = check_if_file_exists(file_request)
            if exists:
                response = construct_response(True)
                connection_socket.send(response.encode())
                bytes_read = open(return_file(file_request), "rb").read()
                connection_socket.sendall(bytes_read)
                print(response)
            else:
                response = construct_response(False)
                connection_socket.send(response.encode())
                print(response)

        connection_socket.close()


print("Starting Thread 1")
Thread(target=server_thread, args=(1271, "1",)).start()
print("Starting Thread 2")
Thread(target=server_thread, args=(1272, "2",)).start()