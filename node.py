from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from wallet import Wallet
from Blockchain_Classes_Day8 import Blockchain


#creating server
app = Flask(__name__)
CORS(app)  #this app is opened to other clients too


#setting up an end point/route and route has 2 things Path and Type of Request
@app.route('/', methods=['GET'])  #for telling flask to execute this when sending a request
def get_ui():
    return send_from_directory('ui','node.html')


@app.route('/balance',methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            'Message:': 'Fecthed wallet successfully',
            'Funds:': balance
        }
        return jsonify(response),201
    else:
        response = {
            'Message:': 'Loading wallet failed..',
            'Wallet update:': wallet.public_key !=None 
        }
        return jsonify(response), 500


@app.route('/wallet',methods=['POST'])
def create_key():
    wallet.create_key()
    if wallet.save_key(): 
        global blockchain
        blockchain = Blockchain(wallet.public_key,port)
        response = {
            'Response:': 'Keys are saved..',
            'Public Key:': wallet.public_key,
            'Private Key:': wallet.private_key,
            'Funds:': blockchain.get_balance()
        }
        return jsonify(response),201
    else:
        response = {
            'Response:': 'Saving Failed..'
        }
        return jsonify(response),500


@app.route('/wallet',methods=['GET'])
def load_key():
    if wallet.load_key():
        global blockchain
        blockchain = Blockchain(wallet.public_key,port)
        response = {
            "Response:": 'Loading successful..',
            'Public Key:': wallet.public_key,
            'Private Key:': wallet.private_key,
            'Funds:': blockchain.get_balance()
            }
        return jsonify(response), 201
    else:
        response = {
            'Response:': 'Saving Failed..'
        }
        return jsonify(response),500


@app.route('/transaction',methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
            'Message:': 'No wallet set up..'
        }
        return jsonify(response),400
    values = request.get_json()
    if not values:
        response = {
            'Message:': 'No Data Found..'
        }
        return jsonify(response),400
    required_field = ['recipient','amount']
    if not all(field in values for field in required_field):
        response = {
            'Message:': 'All field not available..',
        }
        return jsonify(response),400
    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(wallet.public_key,recipient,amount)
    success = blockchain.add_transaction(recipient,wallet.public_key,signature,amount)
    if success:
        response = {
            'Message:': 'Successfully added a transaction..',
            'transaction:': {
                'sender:': wallet.public_key,
                'recipient:': recipient,
                'amount:': amount,
                'signature:': signature
            },
            'Funds:': blockchain.get_balance()
        }
        return jsonify(response),200
    else:
        response = {
            'Message:': 'Creating a transaction failed..'
        }
        return jsonify(response),500

@app.route('/broadcast-block',methods=['POST'])
def broadcast_block():
    values = request.get_json()             #request gives access to the incoming data, whereas requests is for sending request
    if not values:
        response = {
            'Message': 'No data found...'
        }
        return jsonify(response),400
    if 'block' not in values:
        response = {
            'Message': 'Some data missing...'
        }
        return jsonify(response),400
    block = values['block']
    if block['index'] == blockchain.get_chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {'message:': 'Block Added..'}
            return jsonify(response),201
        else:
            response = {'message:': 'Block seems invalid..'}
            return jsonify(response),409
    elif block['index'] > blockchain.chain[-1].index:
        response = {'message:': 'Blockchain seems to differ from local blockchain..'}
        blockchain.resolve_conflicts = True
        return jsonify(response),200
    else:
        response = {'message:': 'Blockchain seems to be shorter, block not added..'}
        return jsonify(response),409


@app.route('/broadcast-transaction',methods=['POST'])
def broadcast_transaction():
    values = request.get_json()             #request gives access to the incoming data, whereas requests is for sending request
    if not values:
        response = {
            'Message': 'No data found...'
        }
        return jsonify(response),400
    required = ['sender','recipient','amount','signature'] #values is a dictionary as get_json returns dict.
    if not all(key in values for key in required):
        response = {
            'Message': 'Some data missing...'
        }
        return jsonify(response),400
    success = blockchain.add_transaction(values['recipient'],values['sender'],values['signature'],values['amount'], is_receiving=True)
    if success:
        response = {
            'Message:': 'Successfully added a transaction..',
            'transaction:': {
                'sender:': values['sender'],
                'recipient:': values['recipient'],
                'amount:': values['amount'],
                'signature:': values['signature']
            }
        }
        return jsonify(response),200
    else:
        response = {
            'Message:': 'Creating a transaction failed..'
        }
        return jsonify(response),500


@app.route('/mine',methods=['POST']) 
def mine():
    if blockchain.resolve_conflicts:
        response = {'message:': 'Resolve the conflicts first, block not added..'}
        return jsonify(response), 409
    block = blockchain.mine_block() 
    if block!= None: 
        dict_block = block.__dict__.copy()
        dict_block['transaction'] = [tx.__dict__ for tx in dict_block['transaction']]
        response = {
            'Response:':'Block added successfully',
            'Block:': dict_block,
            'Funds:': blockchain.get_balance()
        }
        return jsonify(response),201
    else:
        response = {
            'Response:':'Adding a block failed.',
            'Wallet_update:': wallet.public_key != None 
        }
        return jsonify(response),500

@app.route('/resolve',methods=['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response = {'message:': 'The chain is replced'}
    else:
        response = {'message:': 'Local chain kept..'}
    return jsonify(response),200


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.get_chain()
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block['transaction'] = [tx.__dict__ for tx in dict_block['transaction']]
    return jsonify(dict_chain),200
    

@app.route('/transactions',methods=['GET'])
def get_open_transaction():
    transactions = blockchain.get_open_transaction()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions),200


@app.route('/node',methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'Message:' : 'No data attached'
        }
        return jsonify(response),400
    if 'node' not in values:
        response = {
            'Message:' : 'No node data found'
        }
        return jsonify(response),400
    node = values['node']
    blockchain.add_peer_node(node)
    response = {
        'Message:': 'Node added successfully',
        'All_nodes:':blockchain.get_peer_node()
            }
    return jsonify(response),201

@app.route('/node/<node_url>',methods=['DELETE']) #For deleting we have to pass the node in the path e.g., /node/localhost:5000
def delete_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            'Message:': 'No node found..'
        }
        return jsonify(response),400
    blockchain.remove_node(node_url)
    response = {
            'Message:': 'Node removed',
            'All nodes:': blockchain.get_peer_node()
        }
    return jsonify(response),200

        
@app.route('/node', methods = ['GET'])
def get_nodes():
    nodes = blockchain.get_peer_node()
    response = {
        'All nodes:': nodes
    }
    return jsonify(response),200


#starting the server to listen for incoming request
if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p','--port',type=int,default=5000)
    args = parser.parse_args()
    port = args.port
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key,port)
    app.run(host='0.0.0.0', port=port)