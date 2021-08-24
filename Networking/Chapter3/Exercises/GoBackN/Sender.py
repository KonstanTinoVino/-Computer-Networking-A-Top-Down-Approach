import socket
from socket import *
import Networking.Chapter3.Exercises.StopAndWaitUtility.TCPPacket as packet_class
import pickle
import random
from threading import Thread


def generate_checksum(byte_array, error_bit):
    total = 0
    for word in byte_array:
        total += word
    """
    ~ returns 2's complement as a negative integers so +1 will return 1's complement. 
    An error bit is sometimes added to simulate corruption through the network 
    """
    complement = ~total + 1 + error_bit
    return complement


def generate_packets_to_send(fragments):
    packets = []
    for fragment in fragments:
        a_byte_array = bytearray(fragment, "utf8")
        true_fragment = fragment
        error = 0
        rand = random.randint(0, 10)
        if rand < 5:
            if rand > 2:
                error += 1
            else:
                fragment = fragment + str(rand)
        checksum = generate_checksum(a_byte_array, error)
        packets.append(packet_class.Packet(fragment.encode('UTF-8'), "", checksum, true_fragment))
    return packets


def regenerate_clean_packet(error_packet):
    data = error_packet.actual_data
    a_byte_array = bytearray(data, "utf8")
    checksum = generate_checksum(a_byte_array, 0)
    pack = packet_class.Packet(data.encode('UTF-8'), error_packet.sequence, checksum, data)
    d_gram = pickle.dumps(pack)
    return d_gram


def send_message(clientSocket, dGram):
    clientSocket.send(dGram)
    acknowledgement = clientSocket.recv(1024)
    fragment = pickle.loads(acknowledgement)
    return fragment


# Creating Client Socket and connecting it to the server
server_address = ('localhost', 12000)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(server_address)
clientSocket.settimeout(1)

# Creating the message that is to be sent and splitting it in random segments based on " "
message = "Now is the winter of my discontent, made glorious summer by our son of York"
fragments = message.split(" ")
fragments.append("END")

# Creating packet objects from message segments
print("Creating Packets")
packets = generate_packets_to_send(fragments)
acks = []

print("Sending Packets")
ack_index = 0
nacks = []
ack_index = 0


def sender_thread(packets, nacks, ack_index, N, clientSocket):
    # Send First N Packets
    for i in range(N):
        packet = packets[i]
        packet.sequence = i
        print("Sending packet data: " + packet.data.decode() + " sequence: " + str(packet.sequence))
        dGram = pickle.dumps(packet)
        clientSocket.send(dGram)
    packet_index = N
    condition = True
    while condition:
        if packet_index == ack_index:
            if len(packets) >= packet_index + 1:
                packet = packets[packet_index + 1]
                print("Sending packet data: " + packet.data.decode() + " sequence: " + str(packet.sequence))
                dGram = pickle.dumps(packet)
                clientSocket.send(dGram)
        elif len(nacks) != 0:
            for nack in nacks:
                print("Resending package with seq: " + str(nack))
                packet = packets[nack]
                packet.data = packet.actual_data
                dGram = pickle.dumps(packet)
                clientSocket.send(dGram)


def receiver_thread(nacks, clientSocket, ack_index):
    condition = True
    while condition:
        message = None
        while message is None:
            try:
                acknowledgement = clientSocket.recv(1024)
                fragment = pickle.loads(acknowledgement)
                message = str(fragment.data, 'utf-8')
            except timeout:
                print("Packet Presumed Lost, Resending...")
                nacks.append(ack_index)
        if message != "1":
            if message == "0":
                print("Packet was received with errors")
            else:
                print("ACK was corrupted")
            # Resending the same packet until an ACK is returned
            nacks.append(ack_index)
        else:
            ack_index += 1
            print("Packet received successfully")


# Create a server thread
print("Starting Sender Thread")
Thread(target=sender_thread, args=(packets, nacks, ack_index, 4, clientSocket,)).start()

# Create a server thread
print("Starting Receiver Thread")
Thread(target=receiver_thread, args=(nacks, clientSocket, ack_index,)).start()


clientSocket.close()
