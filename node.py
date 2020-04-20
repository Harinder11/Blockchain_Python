from Blockchain_Classes_Day8 import Blockchain
from verification import Verification
from uuid import uuid4

class Node:
    def __init__(self):
        self.id = 'HSK'
        self.blockchain  = Blockchain(self.id)


    def print_blockchain_element(self):
        #Outputs the blockchain list to the console print (blockchain)
        #print('Complete blockchain is', blockchain)
        for block in self.blockchain.get_chain():
            print('Outputting Block')
            print(block)
        else:
            #this will execute whenever the for loop is over either terminated or finished with all iterables
            print ('-' * 20)

    def listen_for_input(self):
        waiting_for_input =True
        while waiting_for_input:
            print("Please choose")
            print("1: If you want to add a transaction")
            print("2: If you want to add mine a block")
            print("3: If you want to show the blockchain")
            print("4: Check the validity of the transaction")
            print("q: If you want to quit")
            user_choice = self.get_user_choice()
            if user_choice == '1':
                # Takes transaction from user
                tx_data = self.blockchain.get_user_transaction()
                #unpacking tuple tx_data
                #this will unpack the tuple tx_data and store 1st value in recipient and 2nd value in amount.
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.id, amount=amount): #as we were skiping sender so we have to mention the name of the argument i.,e amount
                    print('Added transaction!!!')
                else:
                    print('Failed Transaction!!!')
                print(self.blockchain.get_open_transaction())
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain_element()
            elif user_choice == '4':
                if Verification.verify_alltransactions(self.blockchain.get_open_transaction(), self.blockchain.get_balance):
                    print("All transactions are valid")
                else:
                    print("Transactions are invalid!!!")
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print("Input is invalid, please enter a valid value from the list")
            if not Verification.verify_chain(self.blockchain.get_chain()):
                self.print_blockchain_element()
                print("Invalid Blockchain")
                break
            #String Formatting {:6.2F} 6 reserves 6 places default to the right and .2F says 2 decimal points 
            print('Balance of {} is {:6.2F}'.format(self.id, self.blockchain.get_balance()))
        else:
            #this will execute whenever the while loop is over either terminated or finished with all iterables
            print("User left!!!")

    print('Done!')

    def get_user_choice(self):
        return input("Your choice")

node = Node()
node.listen_for_input()


        