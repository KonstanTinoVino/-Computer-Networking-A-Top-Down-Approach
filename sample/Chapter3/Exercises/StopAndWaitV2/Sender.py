from socket import *
import sample.Chapter3.Exercises.StopAndWaitUtility.TCPPacket as packet
import pickle
import random


server_address = ('localhost', 12000)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(server_address)


packets = []
message = "Now is the winter of my discontent, made glorious summer by our son of York"
fragments = message.split(" ")
fragments.append("END")

print("Creating Packets")


def generate_checksum(byte_array, error_bit):
    total = 0
    for word in byte_array:
        total += word
    complement = ~total + 1 + error_bit
    return complement


for fragment in fragments:
    a_byte_array = bytearray(fragment, "utf8")
    error = 0
    rand = random.randint(0, 10)
    if rand < 5:
        if rand > 2:
            error += 1
        else:
            fragment = fragment + str(rand)
    checksum = generate_checksum(a_byte_array, error)
    packets.append(packet.Packet(fragment.encode('UTF-8'), "", checksum))


for packet in packets:
    print("Sending packet data: " + packet.data.decode())
    dGram = pickle.dumps(packet)
    clientSocket.send(dGram)

