

class Packet:

    def __init__(self, data, sequence, checksum, actual_data):
        self.data = data
        self.sequence = sequence
        self.checksum = checksum
        self.actual_data = actual_data
