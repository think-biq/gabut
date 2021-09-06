#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Utility to export google authenticator accounts.

    2021-∞ (c) blurryroots innovation qanat OÜ. All rights reserved.
    See license.md for details.

    https://think-biq.com
'''

__all__ = ['get_version', 'main']


import argparse
import sys
import json
from getpass import getpass
from . import core, nada, kjuar


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_version():
    return "1.1.0"


def create_output_from_accounts(args, accounts):
    output = ''
    if args.uri or args.qr:
        for account in accounts:
            if args.verbose:
                output += f"{account['name']} ({account['issuer']}): "
            uri = core.create_otp_uri(
                account['type'], account['key'],
                account['name'], account['issuer'],
                account['digits'], account['interval']
            )
            if args.qr:
                output += str(kjuar.Kjuar(uri))
            else:
                output += f'{uri}\n'
    else:
        output += json.dumps(accounts)

    return output


def run_export_command(args):
    accounts = []
    for f in args.file:
        accounts += core.export(f)

    if args.encrypt:
        cipher = None
        if None is args.password:
            cipher = nada.Nada(getpass())
        else:
            cipher = nada.Nada(args.password)
        output = cipher.encrypt(json.dumps(accounts)).decode('utf8')
    else:
        output = create_output_from_accounts(args, accounts)

    print(output)

    return 0


def run_load_command(args):
    decryption_function = None
    if args.decrypt:
        cipher = None
        if None is args.password:
            cipher = nada.Nada(getpass())
        else:
            cipher = nada.Nada(args.password)
        decryption_function = lambda contents: cipher.decrypt(contents).decode('utf8')

    accounts = []
    for f in args.file:
        try:
            accounts += core.load(f, decryption_function)
        except Exception as e:
            eprint(f'While processing {f}, encountered: {e}\nSkipping ...')

    output = create_output_from_accounts(args, accounts)
    print(output)

    return 0


def run_recognize_commnad(args):
    output = ''
    for f in args.file:
        urls = core.recognize(f)
        count = len(urls)
        for i in range(0, count):
            output += urls[i]
            if i+1 < count:
                output += '\n'

    print(output)

    return 0


def create_arg_parser():
    parser = argparse.ArgumentParser('gabut', formatter_class=argparse.RawTextHelpFormatter)
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
        , help='Key used for encryption. (You\'ll be prompted if not specified)'
        , default=None)
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
        , help='Key used for decryption. (You\'ll be prompted if not specified)'
        , default=None)
    load_cmd.add_argument('-u', '--uri'
        , action='store_true'
        , help='Show exported accounts as qr code.'
        , default=False)
    load_cmd.add_argument('-q', '--qr'
        , action='store_true'
        , help='Show exported accounts as qr code.'
        , default=False)

    reco_cmd = subparsers.add_parser('recognize')
    reco_cmd.add_argument('file', metavar='file'
        , type=str
        , nargs='+'
        , help='Files to google authenticator exported qr code images.')

    return parser


def main():
    status = 0

    parser = create_arg_parser()
    args = parser.parse_args()

    if args.version:
        print(get_version())
        sys.exit(status)

    commands = {
        'export': run_export_command,
        'load': run_load_command,
        'recognize': run_recognize_commnad
    }

    if not args.command in commands:
        parser.print_help()
        status = 1
    else:
        status = commands[args.command](args)

    sys.exit(status)


if __name__ == '__main__':
    main()
