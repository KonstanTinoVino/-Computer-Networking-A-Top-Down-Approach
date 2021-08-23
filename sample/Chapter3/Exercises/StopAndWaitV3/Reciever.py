import sample.Chapter2.Exercises.AssignmentHttpServer.Server as server
import sample.Chapter3.Exercises.StopAndWaitUtility.TCPPacket as packet
from threading import Thread
import pickle
import random

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


def roll_for_error():
    rand = random.randint(0, 10)
    if rand < 4:
        print("ACK will be corrupted")
        return 2
    return 0


def server_thread(port):
    print("The server is ready to receive")
    past_sequence = 1;
    while True:
        connection_socket, addr = server_socket.socket.accept()
        condition = True;
        while condition:
            try:
                seq = roll_for_error()
                response = connection_socket.recv(port)
                fragment = pickle.loads(response)
                message = str(fragment.data, 'utf-8')
                sequence_recieved = fragment.sequence
                value = check_checksum(message, fragment.checksum)
                print("-------------------------------------------------------", message, " sequence recieved: ", sequence_recieved, " past sequence: ",past_sequence)
                if value == 0 or past_sequence == sequence_recieved:
                    if past_sequence == sequence_recieved:
                        print("Packet received twice")
                    else:
                        print("Correct Packet")
                    response = seq + 1
                    d_gram = generate_ACK(str(response))
                    connection_socket.send(d_gram)
                    past_sequence = sequence_recieved
                else:
                    print("Packet Corrupted")
                    response = seq + 0
                    d_gram = generate_ACK(str(response))
                    connection_socket.send(d_gram)
                    past_sequence = sequence_recieved
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