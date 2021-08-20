
import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad


class Nada:
    def __init__(self, key):
        self.key = hashlib.md5(key.encode('utf8')).digest()

    def encrypt(self, raw_data):
        iv = get_random_bytes(AES.block_size)
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = pad(raw_data.encode('utf-8'), AES.block_size)
        encrypted_data = self.cipher.encrypt(padded_data)
        msg = iv + encrypted_data
        encoded_msg = base64.b64encode(msg)
        return encoded_msg

    def decrypt(self, encoded_msg):
        msg = base64.b64decode(encoded_msg)
        iv = msg[:AES.block_size]
        encrypted_data = msg[AES.block_size:]
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = self.cipher.decrypt(encrypted_data)
        raw_data = unpad(padded_data, AES.block_size)
        return raw_data