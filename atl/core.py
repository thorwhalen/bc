import hashlib
import json
from time import time


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.currentTransactions = []
        self.nodes = set()  # Set of nodes - only unique values are stored - idempotent.

        # create genesis block.
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash):
        """
        Create a new block in the blockchain.

        :param proof: <int> The proof given by the proof of the work algorithm
        :param previous_hash: (Optional) <str> Hash of the previous block.
        :return: new block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.currentTransactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # Reset the current list of transactions
        self.currentTransactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined block.
        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipient
        :param amount: <int> amount
        :return: <int> index of the block that holds the transaction
        """
        self.currentTransactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        # Returns the last block in the chain.
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block.

        :param block: <dict> block
        :return: <str> hash of the block.
        """

        # Make sure the dictionary is Ordered, otherwise we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple proof of work algorithm
        - find a number 'p' such that hash(pp') contains last 4 leading zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        :param last_block: last block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof: Does hash(last_proof, proof) contains 4 leading zeroes?

        :param last_proof: <int> Previous proof
        :param proof: <int> current proof
        :param last_hash: <str> The hash of the previous block
        :return:<bool> True if correct, false if not
        """
        guess = '{last_proof}{proof}{last_hash}'.format(
            last_proof=last_proof, proof=proof, last_hash=last_hash).encode()
        # guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

