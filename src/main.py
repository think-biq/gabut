#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''    
    Utility to export google authenticator accounts.

    2021-∞ (c) blurryroots innovation qanat OÜ. All rights reserved.
    See license.md for details.

    https://think-biq.com
'''

import sys
import gaeh
import json
import urllib.parse
import argparse
from PIL import Image
from pyzbar import pyzbar
from getpass import getpass
from nada import Nada
from kjuar import Kjuar
from version import version as get_version


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def create_arg_parser():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-v', '--verbose'
		, action='store_true'
		, help='Activate verbose logging.'
		, default=False)
	parser.add_argument('-V', '--version'
		, action='store_true'
		, help='Show version number.'
		, default=False)

	subparsers = parser.add_subparsers(dest='command')

	export_cmd = subparsers.add_parser('export')
	export_cmd.add_argument('file', metavar='file'
		, nargs='+'
		, type=argparse.FileType('rb')
		, help='Files to google authenticator exported qr code images.')
	export_cmd.add_argument('-e', '--encrypt'
		, action='store_true'
		, help='Encrypt account export via AES with given password.'
		, default=False)
	export_cmd.add_argument('-p', '--password'
		, type=str
		, help='Key used for encryption. (You\'ll be prompted if not specified)')
	export_cmd.add_argument('-u', '--uri'
		, action='store_true'
		, help='Show exported accounts as qr code.'
		, default=False)
	export_cmd.add_argument('-q', '--qr'
		, action='store_true'
		, help='Show exported accounts as qr code.'
		, default=False)

	load_cmd = subparsers.add_parser('load')
	load_cmd.add_argument('file', metavar='file'
		, type=str
		, nargs='+'
		, help='Files to google authenticator exported qr code images.')
	load_cmd.add_argument('-d', '--decrypt'
		, action='store_true'
		, help='Decrypt account export via AES with given password.'
		, default=False)
	load_cmd.add_argument('-p', '--password'
		, type=str
		, help='Key used for decryption. (You\'ll be prompted if not specified)')
	load_cmd.add_argument('-u', '--uri'
		, action='store_true'
		, help='Show exported accounts as qr code.'
		, default=False)
	load_cmd.add_argument('-q', '--qr'
		, action='store_true'
		, help='Show exported accounts as qr code.'
		, default=False)

	return parser


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

if __name__ == '__main__':
	status = 0

	parser = create_arg_parser()
	args = parser.parse_args()

	if args.version:
		print(get_version())
		sys.exit(status)

	commands = {'export': run_export_command, 'load': run_load_command}
	if not args.command in commands:
		parser.print_help()
		status = 1
	else:
		status = commands[args.command](args)

	sys.exit(status)