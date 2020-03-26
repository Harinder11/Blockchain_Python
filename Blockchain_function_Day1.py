# Input function
blockchain = []

def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction = [1]):
    blockchain.append([last_transaction, transaction_amount])


def get_user_input():
    return float(input('Your transaction amount please:'))

tx_amount = get_user_input()
add_value(tx_amount)

tx_amount = get_user_input()
add_value(tx_amount, get_last_blockchain_value())

tx_amount = get_user_input()
add_value(tx_amount, get_last_blockchain_value())

print (blockchain)

#With Function, Default Argument and Return
"""
blockchain = []

def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount, last_transaction = [1]):
    blockchain.append([last_transaction, transaction_amount])

add_value(5)
add_value(6.3, get_last_blockchain_value())
add_value(8.4, get_last_blockchain_value())

print (blockchain)
"""

#With Function and Retrun

"""
blockchain = [[1]]

def get_last_blockchain_value():
    return blockchain[-1]


def add_value(transaction_amount):
    blockchain.append([get_last_blockchain_value(), transaction_amount])

add_value(5)
add_value(6.3)
add_value(8.4)

print (blockchain)
#"""

