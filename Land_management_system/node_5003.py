# Module 2 - Create a Cryptocurrency

# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/
# requests==2.18.4: 

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse
import time
# Part 1 - Building a Blockchain

class Blockchain:
   #constructor for the class
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.users= []
        self.create_block(proof = 1, previous_hash = '0',merkle_root=self.find_merkle_root({'name':'yoshi','id':127}))
        self.nodes = set()
        self.user_property={};
        
    #functions to get users
    def get_users(self):
            return self.users
        
    #creating a block
    def create_block(self, proof, previous_hash,merkle_root):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions,
                 'merkle-root':merkle_root}
        self.transactions = []
        self.chain.append(block)
        return block
  #function to find the last block of blockchain
    def get_previous_block(self):
        return self.chain[-1]
  #Consensus Algorithm POW implementation
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    #function to get hash of a block or transaction
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    # checks if current chain is valid or not
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    # function to add a transaction
    def add_transaction(self, buyer_id, seller_id, property_id):
        self.transactions.append({'buyer_id': buyer_id,
                                  'seller_id': seller_id,
                                  'property_id':property_id,
                                  'timestamp':str(datetime.datetime.now())
                                  })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    # checks if user is already registered
    def check_user(self, u_id):
        for x in self.users:
            if((int)(x['user_id'])==(int)(u_id)):
                return -1
                
     #function to register users       
    def register_user(self,u_id,property_id):  
        if self.check_user(u_id) == -1:
            #self.user_property[u_id].append(property_id)
            return -1
        self.users.append({'user_id':u_id,'property_id':property_id})
        if(self.user_property.get(u_id)==None):
            self.user_property[u_id]=property_id
        else:
            self.user_property[u_id].append(property_id)
            return -1
        return u_id
           
           
            
    #function to add a node
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    # function to replace the current chain at a node with longest one in blockchain network if its not the longest already
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    #function to find the merkle root of a block
    def find_merkle_root(self,transactions):
        file_hashes=[]
        for t in transactions:
            h=self.hash(t)
            file_hashes.append(h)
        b=[]
        for m in sorted(file_hashes):
            b.append(m)
        list_len=len(b)

        while list_len %2 !=0:
            b.append(b[-1])
            list_len=len(b)
        secondary=[]
        for k in [b[x:x+2] for x in range(0,len(b),2)]:
            hasher=hashlib.sha256()
            hasher.update((k[0]+k[1]).encode())
            secondary.append(hasher.hexdigest())
        if len(secondary)==1:
            return secondary[0][0:64]
        else:
            return self.find_merkle_root(secondary)
     
            
            
    
            
            
            
            

# Part 2 - Mining our Blockchain
#using flask to send and recieve json requests

# Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    #blockchain.add_transaction(buyer_id = node_address, seller_id = 'Node A', property_id = 1)
    mr=blockchain.find_merkle_root(blockchain.transactions)
    block = blockchain.create_block(proof, previous_hash,mr)
    t=block['transactions']
    for x in t:
        blockchain.user_property[x['buyer_id']].append(x['property_id'])
        blockchain.user_property[x['seller_id']].remove(x['property_id'])
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions'],
                'merkle_root':mr}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200



@app.route('/get_users', methods = ['GET'])
def get_users():
    response = {'users_list':blockchain.users,
                'number_of_users': len(blockchain.users)}
    return jsonify(response), 200

@app.route('/get_usersproperty', methods = ['GET'])
def get_usersproperty():
    response = {'users_list':blockchain.user_property,
               }
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json(cache=False)
    print (json)
    transaction_keys = ['buyer_id', 'seller_id', 'property_id']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    if(blockchain.user_property.get(json['buyer_id'])==None):
        return 'Invalid Buyer ID', 400
    if(blockchain.user_property.get(json['seller_id'])==None):
        return 'Invalid Seller ID', 400
    properties=blockchain.user_property[json['seller_id']]
    if(json['property_id'] not in properties):
        return ' Seller doesnt own this property', 400
     
        
        
    index = blockchain.add_transaction(json['buyer_id'], json['seller_id'], json['property_id'])
   
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/register', methods = ['POST'])
def add_user():
    json = request.get_json(cache=False)
    user_keys = ['user_id','property_id']
    if not all(key in json for key in user_keys):
        return 'Enter Correct details', 400
    user=blockchain.register_user(json['user_id'], json['property_id'])
    
    if (user==-1):
        response = {'message': f'User Already Exists'}
        return jsonify(response), 201
    else:
        response = {'message': f'User:{user} Registered'}
        return jsonify(response), 201
    
@app.route('/transaction_history', methods = ['POST'])
def get_th():
    json1 = request.get_json(cache=False)

    pid=json1['property_id']
    th=[]
    for block in blockchain.chain:
        print(block)
        for txn in block['transactions']:
            if(txn['property_id']==json1['property_id']):
                th.append(txn)
  
    response = {'transaction-history': th}
    return jsonify(response), 201    
        
# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json(cache=False)
    
    nodes = json.get('nodes')
    print(json)
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5003)
