from socket import *
import sample.Chapter3.Exercises.StopAndWaitUtility.TCPPacket as packet
import pickle

server_address = ('localhost', 12000)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(server_address)


packets = []
message = "Now is the winter of my discontent, made glorious summer by our son of York"
fragments = message.split(" ")
fragments.append("END")


print("Creating Packets")
for fragment in fragments:
    packets.append(packet.Packet(fragment.encode('UTF-8'), ""))

for packet in packets:
    print("Sending packet data: " + packet.data.decode())
    dGram = pickle.dumps(packet)
    clientSocket.send(dGram)
