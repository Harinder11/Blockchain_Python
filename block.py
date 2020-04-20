from time import time
import printable

class Block(printable.Printable):
    def __init__(self, index, previous_hash, transaction, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.transaction = transaction
        self.proof = proof
        self.timestamp = time

