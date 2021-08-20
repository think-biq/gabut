#
import sys
import otp_export as otpex
import justonce
from PIL import Image
from pyzbar import pyzbar
from getpass import getpass
import json
from nada import Nada


def test_encryption():
    password = getpass()

    cipher = Nada(password)

    # First let us encrypt secret message
    encrypted = cipher.encrypt("The secretest message here")
    with open('hans.enc', 'wb') as f:
        f.write(encrypted)

    with open('hans.enc', 'rb') as f:
        decrypted = cipher.decrypt(f.read()).decode('utf8')
        print(decrypted)


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

    # Setup record command and options.
    gib_cmd = subparsers.add_parser('store')
    gib_cmd.add_argument('stash', metavar='stash', type=str
        , help='Path to a space, where files will be dropped.')
    gib_cmd.add_argument('-e', '--encrypt'
        , action='store_true'
        , help='Encrypt account export via AES.'
        , default=False)

    # Setup record command and options.
    geb_cmd = subparsers.add_parser('retrieve')
    geb_cmd.add_argument('host', metavar='host', type=str
        , help='Host address to connect to.')
    geb_cmd.add_argument('filepath', metavar='in_file', type=str
        , help='Path to a file to be sent.')
    geb_cmd.add_argument('--port', metavar='p', type=int
        , help='Port to host server on.'
        , default=42042)


    # Setup record command and options.
    alias_cmd = subparsers.add_parser('alias')
    alias_cmd.add_argument('host', metavar='host', type=str
        , help='Host address.')
    alias_cmd.add_argument('alias', metavar='alias', type=str
        , help='Alternative name to remember.')

    return parser


def export_from_qr_image(file_path):
	img = Image.open(file_path)
	results = pyzbar.decode(img)
	output = results[0]
	export_url = output.data.decode('utf8')
	exports = otpex.export_opt_to_json(export_url)

	return exports


def show_uri_qr_code(otp_uri):
    import io
    import qrcode
    qr = qrcode.QRCode()
    qr.add_data(otp_uri)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())


def run_cli(qr_mode=False):
    qr_img_paths = sys.argv[1:]
    accounts = []
    for img_path in qr_img_paths:
        print(f"Processing {img_path} ...")
        ex = export_from_qr_image(img_path)
        accounts += ex['accounts']

    if qr_mode:
        for account in accounts:
            op_type = justonce.OTP_OP_TOTP
            if account['key'] == 'HOTP':
                op_type = justonce.OTP_OP_HOTP

            key = account['key']

            account_name = account['name']

            issuer = account['issuer']

            digits = 6
            if account['digits'] == 'EIGHT':
                digits = 8

            interval = 30

            uri = justonce.generate_otp_uri(
                op_type, key, account_name, issuer, digits, interval
            )

            print(f"{account['name']}@{account['issuer']}")
            #show_uri_qr_code(uri)
    else:
        print(accounts)


if __name__ == '__main__':
    run_cli(True)