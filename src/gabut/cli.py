#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Utility to export google authenticator accounts.

    2021-∞ (c) blurryroots innovation qanat OÜ. All rights reserved.
    See license.md for details.

    https://think-biq.com
'''

__all__ = ['cli']


import argparse
import sys
from . import core


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

def cli():
    status = 0

    parser = create_arg_parser()
    args = parser.parse_args()

    if args.version:
        print(get_version())
        sys.exit(status)

    commands = {
        'export': core.run_export_command,
        'load': core.run_load_command
    }
    if not args.command in commands:
        parser.print_help()
        status = 1
    else:
        status = commands[args.command](args)

    sys.exit(status)


if __name__ == '__main__':
    cli()
