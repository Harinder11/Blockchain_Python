class Printable:
        def __repr__(self):
        #return 'Index: {}, Previous Hash: {}, Transaction: {}, Proof: {}, TimeStamp: {}'.format(self.index, self.previous_hash, self.transaction, self.proof, self.timestamp)
            return str(self.__dict__)