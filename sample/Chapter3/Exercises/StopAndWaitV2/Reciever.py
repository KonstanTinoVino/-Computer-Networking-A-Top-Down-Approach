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


def generate_checksum(byte_array, error_bit):
    total = 0
    for word in byte_array:
        total += word
    complement = ~total + 1 + error_bit
    return complement


def generate_ACK(ack):
    a_byte_array = bytearray(ack, "utf8")
    pack = packet.Packet(ack.encode('UTF-8'), "", generate_checksum(a_byte_array, 0), ack.encode('UTF-8'))
    d_gram = pickle.dumps(pack)
    return d_gram


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
                value = check_checksum(message, fragment.checksum)
                if value == 0:
                    print("Correct Packet")
                    d_gram = generate_ACK("1")
                    connection_socket.send(d_gram)
                else:
                    print("Wrong Packet")
                    print("value----------", value, message)
                    d_gram = generate_ACK("0")
                    connection_socket.send(d_gram)
                if message == "END":
                    print(" No more Information ")
                    condition = False
            except EOFError:
                print(" Premature End Of File ")
                print(" No more Information ")
                condition = False
        connection_socket.close()


print("Starting Thread 1")
Thread(target=server_thread, args=(1271,)).start()