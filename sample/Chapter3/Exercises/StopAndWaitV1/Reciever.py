import sample.Chapter2.Exercises.AssignmentHttpServer.Server as server
import sample.Chapter3.Exercises.StopAndWaitUtility.TCPPacket as packet
from threading import Thread
import pickle

server_socket = server.Server("localhost", 12000, "TCP", 10000)


def server_thread(port, thread):
    print("The server is ready to receive")
    while True:
        connection_socket, addr = server_socket.socket.accept()
        condition = True;
        while condition:
            try:
                response = connection_socket.recv(port)
                fragment = pickle.loads(response)
                print(str(fragment.data, 'utf-8'))
            except EOFError:
                print(" No more Information ")
                condition = False
        connection_socket.close()


print("Starting Thread 1")
Thread(target=server_thread, args=(1271, "1",)).start()