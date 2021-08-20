def calculate_checksum(data, k):
    print("Creating Checksum For Packet")
    # Dividing sent message in packets of k bits.
    c1 = data[0:k]
    c2 = data[k:2 * k]
    c3 = data[2 * k:3 * k]
    c4 = data[3 * k:4 * k]

    # Calculating the binary sum of packets
    Sum = bin(int(c1, 2) + int(c2, 2) + int(c3, 2) + int(c4, 2))[2:]

    # Adding the overflow bits
    if (len(Sum) > k):
        x = len(Sum) - k
        Sum = bin(int(Sum[0:x], 2) + int(Sum[x:], 2))[2:]
    if (len(Sum) < k):
        Sum = '0' * (k - len(Sum)) + Sum

    # Calculating the complement of sum
    Checksum = ''
    for i in Sum:
        if (i == '1'):
            Checksum += '0'
        else:
            Checksum += '1'
    return Checksum


def checkReceiver_checksum(ReceivedMessage, k, Checksum):
    print("Reading Checksum for Packet")
    # Dividing sent message in packets of k bits.
    c1 = ReceivedMessage[0:k]
    c2 = ReceivedMessage[k:2 * k]
    c3 = ReceivedMessage[2 * k:3 * k]
    c4 = ReceivedMessage[3 * k:4 * k]

    # Calculating the binary sum of packets + checksum
    ReceiverSum = bin(int(c1, 2) + int(c2, 2) + int(Checksum, 2) +
                      int(c3, 2) + int(c4, 2) + int(Checksum, 2))[2:]

    # Adding the overflow bits
    if (len(ReceiverSum) > k):
        x = len(ReceiverSum) - k
        ReceiverSum = bin(int(ReceiverSum[0:x], 2) + int(ReceiverSum[x:], 2))[2:]

    # Calculating the complement of sum
    ReceiverChecksum = ''
    for i in ReceiverSum:
        if (i == '1'):
            ReceiverChecksum += '0'
        else:
            ReceiverChecksum += '1'
    return ReceiverChecksum


class Packet:

    def __init__(self, data, sequence):
        print(data)
        print(len(data))
        self.data = data
        self.sequence = sequence
        #self.checksum = calculate_checksum(data, 8)
