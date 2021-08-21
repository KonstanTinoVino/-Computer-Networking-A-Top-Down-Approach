import sample.Chapter2.Exercises.AssignmentHttpServer.Server as server
import sample.Chapter3.Exercises.StopAndWaitUtility.TCPPacket as packet
from threading import Thread
import pickle

server_socket = server.Server("localhost", 12000, "TCP", 10000)


def check_checksum(data, checksum):
    byte_array = bytearray(data, "utf8")
    total = 0
    for word in byte_array:
        total += word
    value = checksum + total
    return value


def server_thread(port):
    print("The server is ready to receive")
    while True:
        connection_socket, addr = server_socket.socket.accept()
        condition = True;
        while condition:
            try:
                response = connection_socket.recv(port)
                fragment = pickle.loads(response)
                message = str(fragment.data, 'utf-8')
                print(message)
                value = check_checksum(message, fragment.checksum)
                if value == 0:
                    print("Correct Packet")
                else:
                    print("Wrong Packet")
                    print("value----------", value)
                if message == "END":
                    print(" No more Information ")
                    condition = False
            except EOFError:
                print(" No more Information ")
                condition = False
        connection_socket.close()


print("Starting Thread 1")
Thread(target=server_thread, args=(1271,)).start()