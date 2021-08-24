# GABuT

Google Authenticator Backup Tool enables you to export OTP accounts from qr codes.

## Examples

### Export accounts to json from screenshot
Runs main script on image at data/example-export.png as input. You can specify multiple screenshot files. All accounts will be merged into one list.

```bash
python src/main.py export data/example-export.png
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
python src/main.py export -u data/example-export.png
```
Result:
```text
otpauth://totp/tesseract?secret=GFCDMNZZIMYTORJZGNCTERKFGAZDERSB&issuer=multiverse&algorithm=SHA1&digits=6&period=30
```

### Export accounts to encrypted json from screenshot

```bash
python src/main.py export -e -p $(cat data/example.key) data/example-export.png
```
Result:
```binary
ipF7Iix72KCQ9g8gd8lUe0L4EBAaxcZfQILjFHwktEDZuS+9LoLFWVDVmH57Nn/L4w7i5ux3f+Y4flpjHAPtEFnL6f2osMTEZnX3H4ar1TQXUxYRoVQCBkmDvcOhWzFuPgmP9WWpWUWlnnUpQgf7UoXlSC8FvRml7q7XgcuKvcbPvKe2sjIT2ET4hws9lhdFPJl4SvlBwXjpFxa46bpPKC9vKJHGXnJ4AePtpD9aS08PNuIRCJRZ5vDCG8lVUcPk
```

### Load encrypted json export

```bash
python src/main.py load -d -p $(cat data/example.key) data/example.enc
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
