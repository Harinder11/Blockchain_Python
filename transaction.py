from collections import OrderedDict
from utility.printable import Printable

class Transaction(Printable):
    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.signature = signature
        self.amount = amount

    def ordered_tx(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('signature', self.signature),('amount', self.amount)])