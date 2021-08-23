import socket
from socket import *
import Networking.Chapter3.Exercises.StopAndWaitUtility.TCPPacket as packet_class
import pickle
import random



def generate_checksum(byte_array, error_bit):
    total = 0
    for word in byte_array:
        total += word
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


server_address = ('localhost', 12000)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(server_address)
clientSocket.settimeout(1)

message = "Now is the winter of my discontent, made glorious summer by our son of York"
fragments = message.split(" ")
fragments.append("END")

print("Creating Packets")
packets = generate_packets_to_send(fragments)


print("Sending Packets")

for packet in packets:
    seq = packets.index(packet) % 2
    packet.sequence = seq
    print("Sending packet data: " + packet.data.decode() + " sequence: " + str(packet.sequence))
    dGram = pickle.dumps(packet)
    message = None
    while message is None:
        try:
            clientSocket.send(dGram)
            acknowledgement = clientSocket.recv(1024)
            fragment = pickle.loads(acknowledgement)
            message = str(fragment.data, 'utf-8')
        except:
            print("Packet Presumed Lost, Resending...")
    if message != "1":
        if message == "0":
            print("Packet was received with errors")
        else:
            print("ACK was corrupted")
        condition = True
        while condition:
            print("Resending Packet")
            dGram = regenerate_clean_packet(packet)
            message = None
            while message is None:
                try:
                    clientSocket.send(dGram)
                    acknowledgement = clientSocket.recv(1024)
                    fragment = pickle.loads(acknowledgement)
                    message = str(fragment.data, 'utf-8')
                except:
                    print("Packet Presumed Lost, Resending...")
            if message == "1":
                condition = False
    else:
        print("Packet received successfully")

clientSocket.close()
