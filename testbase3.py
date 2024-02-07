from cryptography.fernet import Fernet
import hashlib
import base64

def generate_key_from_user_input():
    # Ask the user for input to use as a key seed
    user_input = input("Enter a string as a key: ")

    # Convert the user input to bytes using UTF-8 encoding
    key_seed = user_input.encode('utf-8')

    # Use SHA-256 to derive a 32-byte key from the input
    key = hashlib.pbkdf2_hmac('sha256', key_seed, b'salt', 100000)
    print(key)
    # Use the key to generate a Fernet cipher suite
    cipher_suite = Fernet(base64.urlsafe_b64encode(key))

    return cipher_suite

# Rest of the code remains the same


def encrypt_message(cipher_suite:Fernet, message:str):
    # Encrypt the message
    encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
    return encrypted_message

def decrypt_message(cipher_suite:Fernet, encrypted_message:str):
    # Decrypt the message
    encrypted_message=b'gAAAAABlw8HCy-_a7KKPZXfiespg09ld6KD6YvPPPW28J3bIgDaOXfPCpC1Jkgxch5oqm45HV23XF0DUIoHW0-lLORlYjTPBcg=='
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
    return decrypted_message

# Get the key from user input
cipher = generate_key_from_user_input()

# Get a message from the user
# user_message = input("Enter a message to encrypt: ")

# Encrypt the message
# encrypted_message = encrypt_message(cipher, user_message)
# print("Encrypted Message:", encrypted_message)

# Decrypt the message
decrypted_message = decrypt_message(cipher, "encrypted_message")
print("Decrypted Message:", decrypted_message)
