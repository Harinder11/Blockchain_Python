# Input function
blockchain = []

def get_last_blockchain_value():
    """ Takes the previous Blockchain's value """
    #print('inside get_last_blockchain',len(blockchain))
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

#For loop without range keyword
"""
def verify_chain():
    #Checks the complete blockchain if previous value is there in the next block
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        elif block[0] == blockchain[block_index -1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid
"""
#For loop with Range keyword
def verify_chain():
    #Checks the complete blockchain if previous value is there in the next block
    is_valid = True
    for block_index in range (len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index -1]:
            #print('blockchain[block_index][0]',blockchain[block_index][0])
            #print('blockchain[block_index -1]',blockchain[block_index -1])
            is_valid = True
        else:
            is_valid = False
            break
    return is_valid


def add_transaction(transaction_amount, last_transaction = [1]):
    """ This function adds the user input to the blockchain """
    #Checks if last transaction is empty, as last_transaction is coming from get_last_blockchain_value
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transaction_amount])
    #print("Inside add_transaction block is", blockchain)
    #print('Inside add_transaction lentgh is', len(blockchain))

def get_user_transaction():
    """ Returns the input of the user """
    return float(input('Your transaction amount please:'))

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
    print("2: If you want to show the blockchain")
    print("h: If you want to manipulate the Blockchain")
    print("q: If you want to quit")
    user_choice = get_user_choice()
    if user_choice == '1':
        # Takes transaction from user
        tx_amount = get_user_transaction()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain_element()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print("Input is invalid, please enter a valid value from the list")

    if not verify_chain():
        print_blockchain_element()
        print("Invalid Blockchain")
        break
else:
    #this will execute whenever the while loop is over either terminated or finished with all iterables
    print("User left!!!")
    
print('Done!')