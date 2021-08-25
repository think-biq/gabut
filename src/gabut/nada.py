#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''    
    Utility to export google authenticator accounts.

    2021-∞ (c) blurryroots innovation qanat OÜ. All rights reserved.
    See license.md for details.

    https://think-biq.com
'''

__all__ = ['Nada']


import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class Nada:
    '''
    AES encryption helper class.
    '''

    def __init__(self, key):
        self.key = hashlib.md5(key.encode('utf8')).digest()

    def encrypt(self, raw_data):
        iv = get_random_bytes(AES.block_size)
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = pad(raw_data.encode('utf8'), AES.block_size)
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
