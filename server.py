from flask import Flask, escape, request, render_template, jsonify
import requests, time, json
import Blockchain
import os, boto3
import awsConfig
from flask_cors import CORS
import sqlite3



app = Flask(__name__)
CORS(app)


#Initalize Node Copy Of BlockChain
blockchain = Blockchain.Blockchain([])
# model = open('model/model.json', 'r')
#.............

@app.route('/new_model', methods=['POST'])
def new_model():
    files = request.get_data()
    # files = json.loads(files)
    print(files)

    shards = []
    shards.append(open('static/model/group1-shard1of1.bin', 'r').read())
    blockchain = Blockchain.Blockchain(shard)

    return "Success", 201


@app.route('/submit_params', methods=['POST'])
def new_block():
    tx_data = request.get_json()
    required_fields = ["author", "parameters", "accuracy"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid Parameters data", 404
    tx_data["timestamp"] = time.time()

    # blockchain.add_new_transaction(tx_data)
    prevBlock = blockchain.lastBlock
    currentBlock = Blockchain.Block(prevBlock.index + 1, tx_data["parameters"], tx_data["timestamp"], prevBlock.hash)
    if addBlock(currentBlock):
        return "Success", 201
    else:
        return "Invalid block", 400

@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

@app.route('/home')
def index():
    reqs = awsConfig.getRequests()
    return render_template('index.html', accuracy=blockchain.currentAccuracy, chainLength=blockchain.chainLength, requests=reqs)

@app.route('/last_block', methods=['GET'])
def getlastblock():
    return blockchain.lastBlock.parameters

@app.route('/download_dataset', methods=['GET'])
def download():
    conn = sqlite3.connect('dataset.db')
    c = conn.cursor()
    train = []
    for row in c.execute('SELECT * FROM train ORDER BY RANDOM() LIMIT 500'):
        # print(row[0])
        train.append(row[0])
    # print(train)
    xtrain = []
    ytrain = []
    for t in train:
        t = json.loads(t)
        xtrain.append(t['x'])
        ytrain.append(t['y'])

    test = []
    for row in c.execute('SELECT * FROM test'):
        test.append(row[0])

    xtest = []
    ytest = []
    for t in test:
        t = json.loads(t)
        xtest.append(t['x'])
        ytest.append(t['y'])
    conn.close()

    result = {'train': { 'x': str(xtrain), 'y': str(ytrain)}, 'test': { 'x': str(xtest), 'y': str(ytest) } }
    # print(result)
    return json.dumps(result)
    #print(data)
    # Step 1 = download dataset from AWS

    return jsonify(data)
