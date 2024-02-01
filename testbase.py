from cryptography.fernet import Fernet

class SecureChat:
    def __init__(self, key):
        self.key = key
        self.cipher_suite = Fernet(key)

    def encrypt_message(self, message:str):
        encrypted_message = self.cipher_suite.encrypt(message.encode())
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        decrypted_message = self.cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message

# Example usage
if __name__ == "__main__":
    # Simulate key exchange (in a real-world scenario, this would involve secure key distribution)
    key = Fernet.generate_key()

    alice_chat = SecureChat(key)
    bob_chat = SecureChat(key)

    # Alice sends a message
    alice_message = "Hello, Bob! This is a secure message."
    encrypted_message = alice_chat.encrypt_message(alice_message)
    print(encrypted_message)
    # Bob receives and decrypts the message
    decrypted_message = bob_chat.decrypt_message(encrypted_message)

    print(f"Alice: {alice_message}")
    print(f"Bob (Decrypted): {decrypted_message}")
