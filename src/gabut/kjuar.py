#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Utility to export google authenticator accounts.

    2021-∞ (c) blurryroots innovation qanat OÜ. All rights reserved.
    See license.md for details.

    https://think-biq.com
'''

__all__ = ['Kjuar']


import io
import qrcode


class Kjuar():
    '''
    QR code ascii transcriber.
    '''

    def __init__(self, data=None, border = 1):
        self.qr = qrcode.QRCode()
        if None != data:
            self.add(data)
        self.qr.border = 1

    def add(self, data):
        self.qr.add_data(data)

    def print_ascii(self):
        self.qr.print_ascii()

    def to_ascii(self):
        f = io.StringIO()
        self.qr.print_ascii(out=f)
        f.seek(0)
        return f.read()

    def __str__(self):
        return self.to_ascii()

    def __repr__(self):
        return self.to_ascii()
