	
all: install-otp_export

clean_otp_export:
	@(cd dep/otp_export && rm -rf build dist)

otp_export: clean_otp_export
	@(cd dep/otp_export && python3 setup.py bdist_wheel)

install-otp_export: otp_export
	python3 -m pip uninstall otp_export
	python3 -m pip install dep/otp_export/dist/otp_export-1.0.3-cp39-cp39-macosx_10_15_x86_64.whl

run:
	. bin/activate; python3 src/main.py $(FILES)