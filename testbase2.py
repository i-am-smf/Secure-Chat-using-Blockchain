import hashlib
import json
import time
from flask import Flask, request
import requests
from urllib.parse import urlparse

app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, messages, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.messages = messages
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.messages).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.nodes = set()

    def create_genesis_block(self):
        return Block(0, time.time(), [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_valid_chain(self, chain):
        previous_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            if block.previous_hash != previous_block.hash:
                return False

            if block.hash != block.calculate_hash():
                return False

            previous_block = block
            current_index += 1

        return True

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.is_valid_chain(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False

blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': [vars(block) for block in blockchain.chain],
        'length': len(blockchain.chain)
    }
    return json.dumps(response), 200

@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_latest_block()
    new_index = previous_block.index + 1
    new_timestamp = time.time()
    new_messages = request.json.get('messages', [])
    new_block = Block(new_index, new_timestamp, new_messages, previous_block.hash)
    blockchain.add_block(new_block)
    response = {'message': 'Block mined successfully'}
    return json.dumps(response), 200

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
