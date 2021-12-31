# This is a simple blockchain
# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify  

class Blockchain:
    def __init__(self):
        self.chain = []
        self.creat_block(proof = 1, prev_hash = '0')
        
    def creat_block(self, proof, prev_hash):
        block = {'index' : len(self.chain) + 1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'prev_hash' : prev_hash
                 }
        
        self.chain.append(block)
        return block
    
    def get_prev_block(self,chain):
        return self.chain[-1]
    
    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof == False:
            hash_operation = hashlib.sha3_256(str(new_proof**3 - prev_proof**2).encode()).hexdigest()
            if hash_operation[ : 4] == '0000':
                check_proof = True
            
            else:
                new_proof += 1
            
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha3_256(str(proof**3 - prev_proof**2).encode()).hexdigest()
            if hash_operation[ : 4] != '0000':
                return False
            
            prev_block = block
            block_index += 1
            
        return True
    
app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block(blockchain.chain)
    prev_proof = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash = blockchain.hash(prev_block)
    block = blockchain.creat_block(proof, prev_hash)
    response = {'message' : 'Congratulations, you just mined a block!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'prev_hash' : block['prev_hash']
        }
    return jsonify(response) ,200

@app.route('/get_blockchain', methods = ['GET'])
def get_blockchain():
    response = {'chain' : blockchain.chain,
                'lenght' : len(blockchain.chain)
                }
    return jsonify(response) ,200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid == True:
        response = {'message' : 'All good. The Blockchain is valid.'}
        
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)



