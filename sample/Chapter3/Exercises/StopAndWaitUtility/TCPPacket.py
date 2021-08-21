

class Packet:

    def __init__(self, data, sequence, checksum):
        self.data = data
        self.sequence = sequence
        self.checksum = checksum
