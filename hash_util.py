import json     # keeps data and exchange data, converts python objects(dict,list,tuple etc) to json string
import hashlib as hl  # for generating hash

def hash_string_256(string):
    return hl.sha256(string).hexdigest()

def hash_block(block):
    # For generating hash we have to keep all the values of dictionary last_block into 1 string
    # for key in last_block:
    #    value = last_block[key]
    #    hashed_block = hashed_block + str(value)
    # List Comprehension and join only joins string
    #return '-'.join([str(block[key]) for key in block])
    '''
    sha256 creates 64 character hash: 
    json.dumps(block) its the value that we want to hash and it should be string we have to call encode to convert the string in utf-8 format thats string format 
    the hash generated is a byte hash to convert it to string we use hexdigest()
    Arguments:
        :block: The block that should be hashed
    '''
    #JSON does not supports objects, so we have to convert it into dictionary
    hashable_block = block.__dict__.copy()
    hashable_block['transaction'] = [tx.ordered_tx() for tx in hashable_block['transaction']]
    print('hashable_block is {}'.format(hashable_block))
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
    