#importing functool to use reduce function
from functools import reduce
import hashlib as hl  # for generating hash

import json
import pickle
import requests

from utility.hash_util import hash_block, hash_string_256
from block import Block
from transaction import Transaction
from utility.verification import Verification
from wallet import Wallet

MINING_REWARD = 10

class Blockchain:
    def __init__(self, public_key, node_id):
        #First block of blockchain
        genesis_block = Block(0,'',[],100,0)  #Class
        self.__chain = [genesis_block]        #Private attribute
        self.__open_transaction = []          #Private attribute
        self.public_key = public_key          #public_key_id is the public key passed from Wallet class
        self.__peer_node = set()
        self.node_id = node_id
        self.load_data()
        self.resolve_conflicts = False
        
        
    def get_chain(self):
        return self.__chain[:]

    
    def get_open_transaction(self):
        return self.__open_transaction[:]


    def load_data(self):
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode = 'r') as f: #mode='rb' for pickle
                ##--------------for pickle------------------------
                # file_content = pickle.loads(f.read())
                # #File content will be in same format as we dumped with 'chain' and 'ot'
                # blockchain = file_content['chain']
                # open_transaction = file_content['ot']

                ##-------------------json code--------------------
                updated_blockchain = []
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transaction']] #access block with [] as it is reading from the file where it is in the form of dictionary
                    #converted_tx is now a list of transaction object
                    updated_block = Block(block['index'],block['previous_hash'], converted_tx, block['proof'], block['timestamp'] )
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain
                updated_transactions =[]
                open_transactions = json.loads(file_content[1][:-1])
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'],tx['recipient'],tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transaction = updated_transactions   #open_transaction is also a list of transaction objects
                peer_nodes = json.loads(file_content[2])
                self.__peer_node = set(peer_nodes)
        except (IOError, IndexError):
            pass
        finally:
            print('Cleanup!!!!!')


    def save_data(self):
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode= 'w') as f: #mode='wb' for pickle/writing binary
                #f.write(json.dumps(blockchain))      # blockchain is list of block objects
                savable_blockchain = [block.__dict__ for block in 
                        [Block(block_el.index, block_el.previous_hash,[tx.__dict__ for tx in block_el.transaction],block_el.proof, block_el.timestamp) for block_el in self.__chain]]  #list of dictionaries
                f.write(json.dumps(savable_blockchain))
                f.write('\n')
                savable_tx = [tx.__dict__ for tx in self.__open_transaction] #as open_transaction is list of Transaction objects
                f.write(json.dumps(savable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_node)))
                #-----------------for pickle------------------------------
                #for pickle we keep the data in one object and then pass, as we can't write \n character.
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transaction
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print("Error while saving file!!!")


    def get_last_blockchain_value(self):
        """ Takes the previous Blockchain's value """
        #print('inside get_last_blockchain',len(blockchain))
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]



    def add_transaction(self,recipient, sender, signature, amount = 1.0, is_receiving=True):
        """ This function adds the user input to the blockchain
            default arguments should come at the end.
        Arguments:
            :sender: The sender of the coins
            :recipient: The recipient of the coins
            :amount: amount of coins transfered, default is 1
        """
        #We want to add the transaction to the open_transaction from where we will do mining and dictionary will be best in this scenario.
        # transaction = {
        #     'sender':sender, 
        #     'recipient':recipient, 
        #     'amount':amount
        # }
        if self.public_key == None:
            return False
        transaction = Transaction(sender,recipient,signature,amount)
        if Verification.verify_transaction(transaction, self.get_balance): #as verify_transaction is returning True or False
            self.__open_transaction.append(transaction)
            self.save_data()
            if not is_receiving:
                for node in self.__peer_node:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={'sender':sender,'recipient':recipient,'amount':amount,'signature':signature})
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined, needs resolving')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False


    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transaction, last_hash, proof):
            proof += 1
        return proof


    def get_balance(self,sender=None):
        if sender == None:
            if self.public_key == None:
                return None
            participants = self.public_key
        else:
            participants = sender
        tx_sender = [[tx.amount for tx in  block.transaction 
                                if tx.sender == participants] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transaction 
                                    if tx.sender==participants]
        tx_sender.append(open_tx_sender)
        amount_sent = 0
        print('Value of tx_sender is', tx_sender)
        amount_received = 0
        #We can use reduce function that reduces the list to 1 number that depends on the lambda function what you want
        #in below line of code tx_sum will hold the last value.
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                            if len(tx_amt)>0 else tx_sum + 0, tx_sender, 0)
        # for tx in tx_sender: #tx is a list and tx_sender is list of lists which keeps transactions as list
        #     if len(tx)>0:
        #         amount_sent += tx[0]
        tx_recipient = [[tx.amount for tx in block.transaction
                                    if tx.recipient==participants] for block in self.__chain]
        print('this is tx_recipient ',tx_recipient)
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                                if len(tx_amt)>0 else tx_sum + 0 ,tx_recipient, 0)
        
        # for tx in tx_recipient:
        #     if len(tx)>0:
        #         amount_received += tx[0]
        return amount_received - amount_sent

    def mine_block(self):
        if self.public_key == None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work() # We want to exclude reward transaction thats why we are calculating PoW before adding reward
        '''
            We are putting reward points in open_transaction as for mining block takes open_transaction data
            we can have many open_transaction and then mine them all at a time.
        '''
        # reward_transaction = {
        #     'sender':'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD 
        # }
        reward_transaction = Transaction('MINING',self.public_key,'',MINING_REWARD)
        '''
            We need copied_transaction incase there is some problem with mining the block then the transaction will remain in the 
            open_transaction which is global so we are copying it to local variable. Incase the mining is failed then the global open transaction will not have the invalid value.
        '''
        copied_transaction = self.__open_transaction[:] #Copying open_transaction list to copied_transaction
        for tx in copied_transaction:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transaction.append(reward_transaction)
        block = Block(len(self.__chain),hashed_block,copied_transaction, proof)
        self.__chain.append(block)
        self.__open_transaction = []
        self.save_data()
        for node in self.__peer_node:
            url = 'http://{}/broadcast-block'.format(node)
            converted_block = block.__dict__.copy()
            converted_block['transaction'] = [tx.__dict__() for tx in converted_block['transaction']]
            try:
                response = requests.post(url, json={'block':converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving')
                if response.status_code == 409:
                    self.resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return block


    def add_block(self, block):
        transactions = [Transaction(tx['sender'],tx['recipient'],tx['signature'],tx['amount']) for tx in block['transaction']]
        proof_is_valid = Verification.valid_proof(transactions[:-1], block['previous_hash'], block['proof'])
        hashes_match = hash_block(self.get_chain()[-1] == block['previous_hash'])
        if not proof_is_valid or not hashes_match:
            return False
        converted_block = Block(block['index'], block['previous_hash'],transactions, block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        stored_opentransaction = self.__open_transaction[:]
        for itx in block['transaction']:
            for opentx in stored_opentransaction:
                if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient'] and opentx.amount == itx['amount'] and opentx.signature == itx['signatire']:
                    try:
                        self.__open_transaction.remove(opentx)
                    except ValueError:
                        print('Value already removed..')
        self.save_data()
        return True


    def resolve(self):
        winner_chain = self.__chain
        replace = False
        for node in self.__peer_node:
            url = 'http://{}/chain'.format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(block['index'],block['previous_hash'],[Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transaction']]
                    ,block['proof'],block['timestamp']) for block in node_chain]
                node_chain_length = len(node_chain)
                local_node_length = len(winner_chain)
                if node_chain_length > local_node_length and Verification.verify_chain(node_chain):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
        self.resolve_conflicts = False
        self.__chain = winner_chain
        if replace:
            self.__open_transaction = []
        self.save_data()
        return replace


    def get_user_transaction(self):
        """ Returns the input of the user """
        #As I will be the sender of my coins so no need to take this input
        #tx_sender = input('Enter the sender of the transaction')
        tx_recipient = input('Enter the recipient of the transaction:')
        tx_amount = float(input('Your transaction amount please:'))
        return tx_recipient, tx_amount

    def add_peer_node(self, node):
        """ Adds a new node to the peer node set"""
        self.__peer_node.add(node)
        self.save_data()

    def remove_node(self, node):
        self.__peer_node.discard(node)
        self.save_data()

    def get_peer_node(self):
        """Returns all the peer nodes"""
        return list(self.__peer_node)
