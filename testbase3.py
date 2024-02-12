from cryptography.fernet import Fernet
import hashlib
import base64

def generate_key_from_user_input():
    user_input = input("Enter a string as a key: ")
    key_seed = user_input.encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha256', key_seed, b'salt', 100000)
    cipher_suite = Fernet(base64.urlsafe_b64encode(key))
    return cipher_suite

def encrypt_message(cipher_suite:Fernet, message:str):
    encrypted_message = cipher_suite.encrypt(message.encode('utf-8'))
    return encrypted_message

def decrypt_message(cipher_suite:Fernet, encrypted_message:str):
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
    return decrypted_message

cipher = generate_key_from_user_input()

user_message = input("Enter a message to encrypt: ")

encrypted_message = encrypt_message(cipher, user_message)
print("Encrypted Message:", encrypted_message)

decrypted_message = decrypt_message(cipher, encrypted_message)
print("Decrypted Message:", decrypted_message)
