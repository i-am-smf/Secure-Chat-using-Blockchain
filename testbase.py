from cryptography.fernet import Fernet
import base64
import datetime
class SecureChat:
    def __init__(self):

        self.cipher_suite = Fernet(self.key_generator())

    def encrypt_message(self, message:str):
        encrypted_message = self.cipher_suite.encrypt(message.encode())
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        decrypted_message = self.cipher_suite.decrypt(encrypted_message).decode()
        return decrypted_message

    def key_generator(self):
        timestamp=str(int(datetime.datetime.now().timestamp()))
        mobile_number="917373675313"
        str_key=timestamp+mobile_number
        if len(str_key) > 32 or len(str_key) < 32:
            str_key= '0' * (32 - len(str_key)) + str_key
        print(str_key)
        key=base64.b64encode(f"{str_key}".encode('utf-8'))
        return key
    
    def test_decrypt(self):
        encrypted_message=b'gAAAAABmKeihlSjhokdDD0os21DcZfOcZ_hwtCc1FcMlRhdiQmlAMf5KS3hpevEeao7k8arXeqk5um_1LmSgU71rogHLn7l08q1O8PSPhNN6AIoVtv2e0325YCsbvD93HMfEu_3aBFTf'
        timestamp=str(int(datetime.datetime.now().timestamp()))
        while True:
            
            mobile_number="917373675313"
            str_key=timestamp+mobile_number
            
            if len(str_key) > 32 or len(str_key) < 32:
                str_key= '0' * (32 - len(str_key)) + str_key
            
            print(str_key)
            
            key=base64.b64encode(f"{str_key}".encode('utf-8'))
            try:
                fernet=Fernet(key=key)
                decrypted_message = fernet.decrypt(encrypted_message).decode()
                print(decrypted_message)
                break
            except:
                timestamp=str(int(timestamp)-1)

SecureChat().test_decrypt()

# key = Fernet.generate_key()
# key = base64.b64encode("alllsmnflilmslcovlanmielvloslvms".encode('utf-8'))

# alice_chat = SecureChat()
# bob_chat = SecureChat()

# # Alice sends a message
# alice_message = "Hello, Bob! This is a secure message."
# encrypted_message = alice_chat.encrypt_message(alice_message)

# print(encrypted_message)
# # Bob receives and decrypts the message
# decrypted_message = bob_chat.decrypt_message(encrypted_message)

# print(f"Alice: {alice_message}")
# print(f"Bob (Decrypted): {decrypted_message}")
