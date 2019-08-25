from hashlib import sha256
import time
import json
from flask import Flask, request

class Block:
	def __init__(self, index, parameters, timestamp, previousHash):
		self.index = index
		self.parameters = parameters
		self.timestamp = timestamp
		self.previousHash = previousHash
		self.hash = self.computeHash()

	def computeHash(self):
		blockString = json.dumps(self.__dict__, sort_keys=True)
		return sha256(blockString.encode()).hexdigest()

	def getAccuracy(self):
		# TO-DO: create a accuracy solving function from test data
		return 0.001


class Blockchain:
	threshold = 0.1

	def __init__(self, parameters):
		self.chainLength = 0
		self.chain = []
		self.createGenesisBlock(parameters)
		self.currentAccuracy = self.lastBlock.getAccuracy()

	def createGenesisBlock(self, parameters):
		genesisBlock = Block(0, parameters, time.time(),"0")
		self.chainLength = self.chainLength + 1
		self.chain.append(genesisBlock)

	@property
	def lastBlock(self):
		return self.chain[-1]

	def addBlock(self, block):
		previousHash = self.lastBlock.hash

		if previousHash != block.previousHash:
			return False

		if not self.isValidProof(block):
			return False

		self.chainLength = self.chainLength + 1
		self.chain.append(block)
		self.currentAccuracy = block.getAccuracy()
		return True

	def isValidProof(self, block):
		if block.getAccuracy() - self.currentAccuracy > threshold:
			return True
		return False
