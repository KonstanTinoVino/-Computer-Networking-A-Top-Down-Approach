import Networking.Chapter2.Exercises.AssignmentHttpServer.Server as server
import Networking.Chapter3.Exercises.StopAndWaitUtility.TCPPacket as packet
from threading import Thread
import pickle
import random

# Creating server object
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


def roll_for_loss():
    rand = random.randint(0, 10)
    if rand < 4:
        print("Packet Will be Lost")
        return 1
    return 0


"""
Main Server Thread. 
"""


def server_thread(port):
    print("The server is ready to receive")
    # Variable to hold previous sequence number
    past_sequence = 1
    while True:
        # Accept incoming connection
        connection_socket, addr = server_socket.socket.accept()
        condition = True
        # While receiving data from sender
        while condition:
            try:
                # Randomly generate a value that will determine whether ACK the packet will be lost.
                # if loss == 1 -> ACK packet will be "lost", else it loss == 0 ACK will be sent.
                loss = roll_for_loss()
                # Randomly generate a value that will determine whether the ACK packet will be corrupted.
                # if seq == 2 -> ACK packet will be "corrupted", else it seq == 0 ACK will be OK.
                seq = roll_for_error()
                # Receive from sender
                response = connection_socket.recv(port)
                # Deserialize packet with Pickle
                fragment = pickle.loads(response)
                message = str(fragment.data, 'utf-8')
                sequence_received = fragment.sequence
                # generate checksum chek. If value == 0 package was not corrupted, else -> corrupted
                value = check_checksum(message, fragment.checksum)
                print("-------------------------------------------------------", message, " sequence recieved: ",
                      sequence_received, " past sequence: ", past_sequence)
                # if package was not corrupted or lost sent an ACK
                if (value == 0 or past_sequence == sequence_received) and loss == 0:
                    if past_sequence == sequence_received:
                        print("Packet received twice")
                    else:
                        print("Correct Packet")
                    response = seq + 1
                    d_gram = generate_ACK(str(response))
                    connection_socket.send(d_gram)
                    past_sequence = sequence_received
                # Else if package was corrupted send an NACK, unless loss >0
                else:
                    if loss == 0:
                        print("Packet Corrupted")
                        response = seq + 0
                        d_gram = generate_ACK(str(response))
                        connection_socket.send(d_gram)
                        past_sequence = sequence_received
                # If last message data contains keyword end send final acknowledgement and stop expecting input
                if message == "END":
                    print(" No more Information ")
                    response = seq + 1
                    d_gram = generate_ACK(str(response))
                    connection_socket.send(d_gram)
                    past_sequence = sequence_received
                    condition = False
            # Catch error if sender does not finish sending data with "END" keyword
            except EOFError:
                print(" Premature End Of File ")
                print(" No more Information ")
                condition = False
        connection_socket.close()


# Create a server thread
print("Starting Thread 1")
Thread(target=server_thread, args=(1271,)).start()
