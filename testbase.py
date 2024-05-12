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
        encrypted_message=b'gAAAAABmQMPa82A08kuhp4VPU-kHoowQgLFHTyESOG4zJWZ3-rr6Qd5GU5xF_JbwhDdsCVhac5HHSwOAY2lvJErdwtxCAOW00Tyx5ScKQGjbUGbxbdfL0S8='
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

# data=SecureChat().encrypt_message("Hello Prem")
# print(data)
