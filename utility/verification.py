from utility.hash_util import hash_block, hash_string_256
from wallet import Wallet

class Verification:
    @staticmethod
    def valid_proof(transaction, last_hash, proof):
        guess = (str([tx.ordered_tx for tx in transaction]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[0:2] == '00'


    @classmethod
    def verify_chain(cls, blockchain):
        #Checks the complete blockchain if previous value is there in the next block
        for (index,block) in enumerate(blockchain): #enumirate gives the tuple with index an data
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index-1]):
                '''
                block['previous'] current block keeps the complete blockchain info.
                blockchain[index-1] as hash of present block is the complete info of blockchain except the present block. 
                '''
                return False
                '''
                we are also verifying if the transaction, previous hash and proof lead to the valid hash or not
                we already know the proof number, we don't want to include the reward transaction so we have block['transaction'][:-1] because while mining we had calculated the 
                proof without adding the reward transaction and here we are just checkig if we are getting the valid hasg('00') with transaction, previous hash and the proof number that we had calculated.
                '''
            if not cls.valid_proof(block.transaction[:-1], block.previous_hash, block.proof):
                print('Proof of Work not valid')
                return False
            
        return True


    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds = True):
        if check_funds:
            sender_balance = get_balance(transaction.sender)
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction) #this line work same as the below commented lines will do
        else:
            return Wallet.verify_transaction(transaction)
        '''
        if sender_balance >= transaction['amount']
            return True
        else:
            return False
        '''


    @classmethod
    def verify_alltransactions(cls, open_transaction, get_balance):
        #returns true if all transaction are valid
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transaction])  #No need to check for funds here, so the new argument False is passed