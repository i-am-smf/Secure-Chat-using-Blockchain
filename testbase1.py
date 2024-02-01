from cryptography.fernet import Fernet
import hashlib
import json
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self.chain.append(block)
        return block

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof


class SecureChat:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.blockchain = Blockchain()

    def encrypt_message(self, message:str):
        encrypted_message = self.cipher_suite.encrypt(message.encode())
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        decrypted_message = self.cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message

    def send_message(self, sender, recipient, message):
        previous_block = sender.blockchain.get_previous_block()
        proof = sender.blockchain.proof_of_work(previous_block['proof'])
        previous_hash = sender.blockchain.hash(previous_block)
        block = sender.blockchain.create_block(proof, previous_hash)

        encrypted_message = recipient.encrypt_message(message)

        return {
            'sender': sender,
            'recipient': recipient,
            'encrypted_message': encrypted_message,
            'block': block
        }

# Example usage
if __name__ == "__main__":
    alice = SecureChat()
    bob = SecureChat()

    # Alice sends a secure message to Bob
    message_to_bob = "Hello, Bob! This is a secure message."
    message_info = alice.send_message(alice, bob, message_to_bob)

    # Bob receives and decrypts the message
    decrypted_message = bob.decrypt_message(message_info['encrypted_message'])

    print(f"Alice: {message_to_bob}")
    print(f"Bob (Decrypted): {decrypted_message}")
