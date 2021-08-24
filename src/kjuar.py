#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""    
    Utility to export google authenticator accounts.

    2021-∞ (c) blurryroots innovation qanat OÜ. All rights reserved.
    See license.md for details.

    https://think-biq.com
"""
import io
import qrcode


class Kjuar():

    def __init__(self):
        self.qr = qrcode.QRCode()

    def add(self, data):
        self.qr.add_data(data)

    def __repr__(self):
        f = io.StringIO()
        self.qr.print_ascii(out=f)
        f.seek(0)
        return f.read()
