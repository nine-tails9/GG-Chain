from flask import Flask, escape, request, render_template, jsonify
import requests, time, json
import Blockchain
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
peers = []
#Initalize Node Copy Of BlockChain
blockchain = Blockchain.Blockchain()
#.............

@app.route('/submit_params', methods=['POST'])
def new_block():
    tx_data = request.get_json()
    required_fields = ["author", "parameters"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invlaid Parameters data", 404
    tx_data["timestamp"] = time.time()



    # blockchain.add_new_transaction(tx_data)
    prevBlock = blockchain.lastBlock
    # currentBlock = Blockchain.Block(tx_data["parameters"], )

    return "Success", 201

@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

@app.route('/add_nodes', methods=['POST'])
def register_new_peers():
    nodes = request.get_json()
    if not nodes:
        return "Invalid data", 400
    for node in nodes:
        peers.add(node)
    return "Success", 201

# def consensus():
#     global blockchain

#     longest_chain = None
#     current_len = len(blockchain)

#     for node in peers:
#         response = requests.get('http://{}/chain'.format(node))
#         length = response.json()['length']
#         chain = response.json()['chain']
#         if length > current_len and blockchain.check_chain_validity(chain):
#             current_len = length
#             longest_chain = chain

#     if longest_chain:
#         blockchain = longest_chain
#         return True

#     return False
def validate_and_add_block(block_data):

    prev_block = getPrevBlock()
    if acc > prev_block['accuray']:
        proof = block_data['hash']
        added = blockchain.add_block(block, proof)
    else:
        return "The block was discarded by the node", 400
    announce_new_block(added)
    return "Block added to the chain", 201

def announce_new_block(block):
    for peer in peers:
        url = "http://{}/add_block".format(peer)
        requests.post(url, data=json.dumps(block.__dict__, sort_keys=True))
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/download_dataset', methods=['GET'])
def download():
    data = {'author': "Deepanshu", "Year": "3rd"}
    return jsonify(data)
