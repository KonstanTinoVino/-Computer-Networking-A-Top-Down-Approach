import socket
from socket import *
import Networking.Chapter3.Exercises.StopAndWaitUtility.TCPPacket as packet_class
import pickle
import random


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


print("Sending Packets")


for packet in packets:
    # Calculating modulo of packet index within the array to get seq 0 or 1 and setting the packet's sequence number
    seq = packets.index(packet) % 2
    packet.sequence = seq
    print("Sending packet data: " + packet.data.decode() + " sequence: " + str(packet.sequence))
    # Serializing packet contents for sending using pickle
    dGram = pickle.dumps(packet)
    # Attempt to send message through socket.
    # If a packet gets lost (socket timed out), it attempts to send the same information again
    message = None
    while message is None:
        try:
            fragment = send_message(clientSocket, dGram)
            message = str(fragment.data, 'utf-8')
        except timeout:
            print("Packet Presumed Lost, Resending...")
    # If message data is anything but 1 it is assumed that the packet was corrupted or the ACK was corrupted
    if message != "1":
        if message == "0":
            print("Packet was received with errors")
        else:
            print("ACK was corrupted")
        condition = True
        # Resending the same packet until an ACK is returned
        while condition:
            print("Resending Packet")
            dGram = regenerate_clean_packet(packet)
            # Attempt to send message through socket.
            # If a packet gets lost (socket timed out), it attempts to send the same information again
            message = None
            while message is None:
                try:
                    fragment = send_message(clientSocket, dGram)
                    message = str(fragment.data, 'utf-8')
                except timeout:
                    print("Packet Presumed Lost, Resending...")
            if message == "1":
                condition = False
    else:
        print("Packet received successfully")

clientSocket.close()
