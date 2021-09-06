# GABuT

Google Authenticator Backup Tool enables you to export OTP accounts from qr codes.

## Example Data

You can find an example google authenticator export at *data/example.png*.

<img src="data/example.png" alt="Example google authenticator export" height="512"/>

## Setup

To run gabut locally, make sure the virtual environment is properly setup and all requirements are installed by running:
```bash
make prepare
```
And then activate the virtual environment run the cli tool via:
```bash
. bin/activate
python3 gabut.py -V
```

When installed you can simply use:
```bash
gabut -V
```

## Examples

### Recognize google backup url
Checks an image for a google authenticator backup qr code and prints the urls found within the image.

```bash
gabut recognize data/example.png
```
Example result:
```bash
otpauth-migration://offline?data=CjMKFDFENjc5QzE3RTkzRTJFRTAyMkZBEgl0ZXNzZXJhY3QaCm11bHRpdmVyc2UgASgBMAIQARgBIAA%3D
```


### Export accounts to json from screenshot
Runs main script on image at data/example.png as input. You can specify multiple screenshot files. All accounts will be merged into one list.

```bash
gabut export data/example.png
```
Result:
```json
[
  {
    "type": "totp",
    "key": "GFCDMNZZIMYTORJZGNCTERKFGAZDERSB",
    "name": "tesseract",
    "issuer": "multiverse",
    "digits": 6,
    "algorithm": "SHA1",
    "counter": 0,
    "interval": 30
  }
]
```

### Export to otpauth uris from screenshot

```bash
gabut export -u data/example.png
```
Result:
```text
otpauth://totp/tesseract?secret=GFCDMNZZIMYTORJZGNCTERKFGAZDERSB&issuer=multiverse&algorithm=SHA1&digits=6&period=30
```

### Export accounts to encrypted json from screenshot

As good practice, make sure to not put your password into the command directly, so it can't be retrived throuth the shell history or process list.

```bash
gabut export -e -p $(cat data/example.key) data/example.png
```
Result:
```binary
ipF7Iix72KCQ9g8gd8lUe0L4EBAaxcZfQILjFHwktEDZuS+9LoLFWVDVmH57Nn/L4w7i5ux3f+Y4flpjHAPtEFnL6f2osMTEZnX3H4ar1TQXUxYRoVQCBkmDvcOhWzFuPgmP9WWpWUWlnnUpQgf7UoXlSC8FvRml7q7XgcuKvcbPvKe2sjIT2ET4hws9lhdFPJl4SvlBwXjpFxa46bpPKC9vKJHGXnJ4AePtpD9aS08PNuIRCJRZ5vDCG8lVUcPk
```

### Load encrypted json export

```bash
gabut load -d -p $(cat data/example.key) data/example.enc
```
Result:
```json
[
  {
    "type": "totp",
    "key": "GFCDMNZZIMYTORJZGNCTERKFGAZDERSB",
    "name": "tesseract",
    "issuer": "multiverse",
    "digits": 6,
    "algorithm": "SHA1",
    "counter": 0,
    "interval": 30
  }
]
```
