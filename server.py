from flask import Flask, escape, request, render_template, jsonify
import requests, time, json
import Blockchain
import os, boto3
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
peers = []

client = boto3.client('dynamodb', aws_access_key_id='ASIA2FMJGGTU6Y4SVC45', aws_secret_access_key='XrK+igsVW4t1/oWh6AjTzs3JrM+j5A/C/Xry0ZAQ',
aws_session_token='FQoGZXIvYXdzEIL//////////wEaDH24zWl1MtRAqoYNHyKDAh7ZIZ3OYeg6IqtSLqMh31Czis49Of9ArHGggKiyBpyQMNyEe984hVAeA3ski5RwP5vyhzy50qPvxO3YRzUSwIMXOYaP+GNQYJU80X9Ep16rgP/SSoGqhkLEj+oYcafbGTuYwWz/suTPC0vgYTplW67OxCgBRSqwUKBeBKQJSIg/uAxezAaf/OI6v9lAjXxVqNPIdSAYASHDOJG64DvGUq4EkB9M8XyGyjgl03Y2EFfrHVAU8dh6yjEC3J737Lb3N7y2GJVcMp7i1mBPL8thKGh8EmwVHxeyWoU+j+g2YioqLhZv5rwlbpn4aQieO6EXrCDHOJUE+VqKEF5JwRK5sDpfCscor8SF6wU=')
client.put_item(
TableName='models',
Item = {"id": {"S": "1" }, "name": {"S": "Deepanshu "} }
)
#Initalize Node Copy Of BlockChain
#blockchain = Blockchain.Blockchain()
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
    #print(data)
    # Step 1 = download dataset from AWS

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/model", "model.json")
    data = json.load(open(json_url))
    return jsonify(data)
