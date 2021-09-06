#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''    
    Utility to export google authenticator accounts.

    2021-∞ (c) blurryroots innovation qanat OÜ. All rights reserved.
    See license.md for details.

    https://think-biq.com
'''

__all__ = ['export_otpauth_uri_from_qr_image', 'create_otp_uri', 'export', 'load']


import sys
import gaeh
import json
import urllib.parse
from PIL import Image
from pyzbar import pyzbar


def export_otpauth_uri_from_qr_image(file_path):
    img = Image.open(file_path)
    otpauth_exports = []
    for recognition in pyzbar.decode(img):
        otpauth_exports.append(recognition.data.decode('utf8'))
    return otpauth_exports


def create_otp_uri(otp_type, key, account_name, issuer, digits=6, interval=30, algo="SHA1"):
    sec_name = urllib.parse.quote(account_name)
    base = f"otpauth://{otp_type}/{sec_name}"
    sec_issuer = urllib.parse.quote(issuer)
    args = f"?secret={key}&issuer={sec_issuer}&algorithm={algo}&digits={digits}&period={interval}"
    return base + args


def recognize(img_path):
    '''Recognizes google authenticator backup url from qr image. Returns a list.'''
    return export_otpauth_uri_from_qr_image(img_path)


def export(img_path):
    exported_accounts = []

    for url in recognize(img_path):
        exports = gaeh.export_otp_accounts(url)
        exported_accounts += exports['accounts']

    accounts = []
    for raw_account in exported_accounts:
        account = {
            'type': 'hotp' if 'HOTP' == raw_account['key'] else 'totp',
            'key': raw_account['key'],
            'name': raw_account['name'],
            'issuer': raw_account['issuer'],
            'digits': 8 if 'EIGHT' == raw_account['digits'] else 6,
            'algorithm': raw_account['algorithm'],
            'counter': raw_account['counter'],
            'interval': 30
        }
        accounts.append(account)

    return accounts


def load(file, decryption_function = None):
    accounts = []
    with open(file, 'rb') as f:
        contents = f.read()
        if decryption_function:
            contents = decryption_function(contents)
        try:
            accounts += json.loads(contents)
        except json.decoder.JSONDecodeError as e:
            raise Exception(f'File contents is no valid json! ({e})')

    return accounts
