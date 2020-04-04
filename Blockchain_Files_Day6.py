#importing functool to use reduce function
from functools import reduce
import hashlib as hl  # for generating hash
from collections import OrderedDict

import json
import pickle

from hash_util import hash_block, hash_string_256

MINING_REWARD = 10
#First block of blockchain
genesis_block = {
        'previous_hash': '',
        'index' : 0,
        'transaction': [],
        'proof': 100
    }
blockchain = [genesis_block]
open_transaction = []
owner = 'Harinder' #We will be sender for our coins
participants = {'Harinder'}


def load_data():
    with open('blockchain.txt', mode = 'r') as f: #mode='rb' for pickle
        global blockchain
        global open_transaction
        ##--------------for pickle------------------------
        # file_content = pickle.loads(f.read())
        # #File content will be in same format as we dumped with 'chain' and 'ot'
        # blockchain = file_content['chain']
        # open_transaction = file_content['ot']

        ##-------------------json code--------------------
        updated_blockchain = []
        updated_openblockchain = []
        file_content = f.readlines()
        blockchain = json.loads(file_content[0][:-1])
        for block in blockchain:
            updated_block = {
                'previous_hash':block['previous_hash'],
                'index': block['index'],
                'proof': block['proof'],
                'transaction': [OrderedDict(
                    [('sender', tx['sender']), ('recipient',tx['recipient']),('amount', tx['amount'])]) for tx in block['transaction']]
            }
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain
        open_transaction = json.loads(file_content[1])
        for tx in open_transaction:
            updated_openblock = OrderedDict(
                    [('sender', tx['sender']), ('recipient',tx['recipient']),('amount', tx['amount'])])
            updated_openblockchain.append(updated_openblock)
        open_transaction = updated_openblockchain


load_data()

def save_data():
    with open('blockchain.txt', mode= 'w') as f: #mode='wb' for pickle/writing binary
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transaction))
        #-----------------for pickle------------------------------
        #for pickle we keep the data in one object and then pass, as we can't write \n character.
        # save_data = {
        #     'chain': blockchain,
        #     'ot': open_transaction
        # }
        # f.write(pickle.dumps(save_data))


def get_last_blockchain_value():
    """ Takes the previous Blockchain's value """
    #print('inside get_last_blockchain',len(blockchain))
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

#For loop with Range keyword
def verify_chain():
    #Checks the complete blockchain if previous value is there in the next block
    for (index,block) in enumerate(blockchain):#enumirate gives the tple with index an data
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
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
        if not valid_proof(block['transaction'][:-1], block['previous_hash'], block['proof']):
            print('Proof of Work not valid')
            return False
        
    return True


def add_transaction(recipient, sender = owner, amount = 1.0):
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
    transaction = OrderedDict(
        [('sender', sender), ('recipient',recipient),('amount', amount)]
    )
    if verify_transaction(transaction): #as verify_transaction is returning True or False
        open_transaction.append(transaction)
        save_data()
        participants.add(sender) #Taking values from arguments
        participants.add(recipient) #Taking values from arguments
        return True
    return False

def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount'] #this line work same as the below commented lines will do
    '''
    if sender_balance >= transaction['amount']
        return True
    else:
        return False
    '''

def verify_alltransactions():
    #returns true if all transaction are valid
    return all([verify_transaction(tx) for tx in open_transaction])

    
def valid_proof(transaction, last_hash, proof):
    guess = (str(transaction) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transaction, last_hash, proof):
        proof += 1
    return proof


def get_balance(participants):
    tx_sender = [[tx['amount'] for tx in  block['transaction'] 
                            if tx['sender'] == participants] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transaction 
                                   if tx['sender']==participants]
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
    tx_recipient = [[tx['amount'] for tx in block['transaction'] 
                                  if tx['recipient']==participants] for block in blockchain]
    print('this is tx_recipient ',tx_recipient)
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                             if len(tx_amt)>0 else tx_sum + 0 ,tx_recipient, 0)
    
    # for tx in tx_recipient:
    #     if len(tx)>0:
    #         amount_received += tx[0]
    return amount_received - amount_sent

def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work() # We want to exclude reward transaction thats why we are calculating PoW before adding reward
    '''
        We are putting reward points in open_transaction as for mining block takes open_transaction data
        we can have many open_transaction and then mine them all at a time.
    '''
    # reward_transaction = {
    #     'sender':'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD 
    # }
    reward_transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)]
    )
    '''
        We need copied_transaction incase there is some problem with mining the block then the transaction will remain in the 
        open_transaction which is global so we are copying it to local variable. Incase the mining is failed then the global open transaction will not have the invalid value.
    '''
    copied_transaction = open_transaction[:] #Copying open_transaction list to copied_transaction
    copied_transaction.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index' : len(blockchain),
        'transaction': copied_transaction,
        'proof': proof

    }
    blockchain.append(block)
    return True

def get_user_transaction():
    """ Returns the input of the user """
    #As I will be the sender of my coins so no need to take this input
    #tx_sender = input('Enter the sender of the transaction')
    tx_recipient = input('Enter the recipient of the transaction:')
    tx_amount = float(input('Your transaction amount please:'))
    return tx_recipient, tx_amount


def get_user_choice():
    return input("Your choice")

def print_blockchain_element():
    #Outputs the blockchain list to the console print (blockchain)
    print('Complete blockchain is', blockchain)
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        #this will execute whenever the for loop is over either terminated or finished with all iterables
        print ('-' * 20)
waiting_for_input =True

while waiting_for_input:
    print("Please choose")
    print("1: If you want to add a transaction")
    print("2: If you want to add mine a block")
    print("3: If you want to show the blockchain")
    print("4: Show all participants")
    print("5: Check the validity of the transaction")
    print("h: If you want to manipulate the Blockchain")
    print("q: If you want to quit")
    user_choice = get_user_choice()
    if user_choice == '1':
        # Takes transaction from user
        tx_data = get_user_transaction()
        #unpacking tuple tx_data
        #this will unpack the tuple tx_data and store 1st value in recipient and 2nd value in amount.
        recipient, amount = tx_data
        if add_transaction(recipient,amount=amount): #as we were skiping sender so we have to mention the name of the argument i.,e amount
            print('Added transaction!!!')
        else:
            print('Failed Transaction!!!')
        print(open_transaction)
    elif user_choice == '2':
        if mine_block():
            open_transaction = []
            save_data()
    elif user_choice == '3':
        print_blockchain_element()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_alltransactions:
            print("All transactions are valid")
        else:
            print("Transactions are invalid!!!")
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                                'previous_hash': '',
                                'index' : 0,
                                'transaction': [{'sender': 'BSK', 'recipient': 'SKK', 'amount': 100}]
                            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print("Input is invalid, please enter a valid value from the list")

    if not verify_chain():
        print_blockchain_element()
        print("Invalid Blockchain")
        break
    #String Formatting {:6.2F} 6 reserves 6 places default to the right and .2F says 2 decimal points 
    print('Balance of {} is {:6.2F}'.format('Harinder', get_balance('Harinder')))
else:
    #this will execute whenever the while loop is over either terminated or finished with all iterables
    print("User left!!!")
    
print('Done!')