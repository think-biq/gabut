#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''    
    Utility to export google authenticator accounts.

    2021-∞ (c) blurryroots innovation qanat OÜ. All rights reserved.
    See license.md for details.

    https://think-biq.com
'''

__all__ = ['run_load_command', 'run_export_command']


import sys
import gaeh
import json
import urllib.parse
from PIL import Image
from pyzbar import pyzbar
from getpass import getpass
from .nada import Nada
from .kjuar import Kjuar
from .version import version as get_version


def export_otpauth_from_qr_image(file_path):
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


def create_output_from_accounts(accounts):
    output = ''
    if args.uri:
        for account in accounts:
            uri = create_otp_uri(
                account['type'], account['key'],
                account['name'], account['issuer'], 
                account['digits'], account['interval']
            )
            
            if args.verbose:
                output += f"{account['name']} ({account['issuer']})"

            if args.qr:
                k = Kjuar()
                k.add(uri)
                output += str(k)
            else:
                output += uri
    else:
        output += json.dumps(accounts)
    
    return output


def run_export_command(args):
    exported_accounts = []
    for img_path in args.file:
        for url in export_otpauth_from_qr_image(img_path):
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

    if args.encrypt:
        password = args.password
        if password is None:
            password = getpass()
        cipher = Nada(password)
        encrypted = cipher.encrypt(json.dumps(accounts))
        print(encrypted.decode('utf8'))

        return 0

    output = create_output_from_accounts(accounts)
    print(output)

    return 0


def run_load_command(args):
    cipher = None
    if args.decrypt:
        password = args.password
        if None is password:
            password = getpass()
        cipher = Nada(password)

    exported_accounts = []
    for file_path in args.file:
        with open(file_path, 'rb') as f:
            contents = f.read()
            if cipher:
                contents = cipher.decrypt(contents).decode('utf8')
            try:
                file_accounts = json.loads(contents)
            except json.decoder.JSONDecodeError as e:
                eprint(f'File contents is no valid json! ({e})')
                return 1

            exported_accounts += file_accounts

    output = create_output_from_accounts(exported_accounts)
    print(output)

    return 0
