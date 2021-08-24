"""
Packet object to hold data between transmission
"""


class Packet:

    def __init__(self, data, sequence, checksum, actual_data):
        self.data = data
        self.sequence = sequence
        self.checksum = checksum
        # Since corruption is simulated by randomly modifying the data variable,
        # actual_data contains the uncorrupted value whenever a NACK.
        self.actual_data = actual_data
