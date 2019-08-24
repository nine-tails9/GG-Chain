from hashlib import sha256
import time
import json

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
		return 0


class Blockchain:
	threshold = 0.1

	def __init__(self):
		self.chain = []
		self.createGenesisBlock()
		self.currentAccuracy = self.lastBlock.getAccuracy()

	def createGenesisBlock(self):
		genesisBlock = Block(0, [], time.time(),"0")
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

		self.chain.append(block)
		self.currentAccuracy = block.getAccuracy()
		return True

	def isValidProof(self, block):
		if block.getAccuracy() - self.currentAccuracy > threshold:
			return True
		return False

