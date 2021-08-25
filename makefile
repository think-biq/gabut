#
#    Google Authenticator Export Helper.
#
#    2021-∞ (c) blurryroots innovation qanat OÜ. All rights reserved.
#    See license.md for details.
#
#    https://think-biq.com

FILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
PROJECT_DIR := $(shell dirname $(FILE_PATH))
PROJECT_NAME := $(notdir $(patsubst %/,%,$(dir $(FILE_PATH))))

DEBUG_FLAG :=
BUILD_PATH = "${PROJECT_DIR}/build"

ifeq '$(findstring ;,$(PATH))' ';'
	OS = "win"
	VENV_BIN_DIR = Scripts
	STD_FLAG = "/std:c++17 /EHa"
	EXE_NAME = gaeh
	BUILD_PATH_RELEASE = "${BUILD_PATH}/Release"
	EXE_PATH_RELEASE = "${BUILD_PATH_RELEASE}/${EXE_NAME}"
	BUILD_PATH_DEBUG = "${BUILD_PATH}/Debug"
	EXE_PATH_DEBUG = "${BUILD_PATH_DEBUG}/${EXE_NAME}"
	LLDB = lldb
	PYTHON = python
	PYTHON_EXECUTABLE := "${shell $(PYTHON) -c "import sys; print(sys.executable)"}"
else
	OS = "unix-y"
	VENV_BIN_DIR = bin
	STD_FLAG = "--std=c++17"
	EXE_NAME = gaeh
	BUILD_PATH_RELEASE = "${BUILD_PATH}"
	EXE_PATH_RELEASE = "${BUILD_PATH_RELEASE}/${EXE_NAME}"
	BUILD_PATH_DEBUG = "${BUILD_PATH}"
	EXE_PATH_DEBUG = "${BUILD_PATH_DEBUG}/${EXE_NAME}"
	LLDB = lldb
	PYTHON := python3
	PYTHON_EXECUTABLE := $(shell which $(PYTHON))
endif

CMD_ACTIVATE_VENV = . "$(PROJECT_DIR)/$(VENV_BIN_DIR)/activate"
CMD_DEACTIVATE_VENV = declare -f deactivate > /dev/null && deactivate || true


all: prepare install-gaeh build-wheel

prepare:
	@$(CMD_DEACTIVATE_VENV); $(PYTHON) -m venv $(PROJECT_DIR)
	$(CMD_ACTIVATE_VENV); $(PYTHON) -m pip install -U pip
	$(CMD_ACTIVATE_VENV); find . -iname "requirements.txt" -exec $(PYTHON) -m pip install -r {} \;

clean:
	rm -rf $(PROJECT_DIR)/{bin,include,lib,pyvenv.cfg}

clean-gaeh:
	@$(CMD_ACTIVATE_VENV); (cd dep/gaeh && rm -rf build dist)

build-gaeh: clean-gaeh
	@$(CMD_ACTIVATE_VENV); (\
		cd dep/gaeh \
		&& pip install -r requirements.txt \
		&& $(PYTHON) setup.py bdist_wheel\
	)

install-gaeh: build-gaeh
	@$(CMD_ACTIVATE_VENV); $(PYTHON) -m pip uninstall --yes gaeh
	$(CMD_ACTIVATE_VENV); $(PYTHON) -m pip install gaeh \
		--force-reinstall --no-index --find-links="file://$(PROJECT_DIR)/dep/gaeh/dist"

build-wheel:
	$(CMD_ACTIVATE_VENV); python3 setup.py bdist_wheel

install-wheel: build-wheel
	$(CMD_ACTIVATE_VENV); python3 -m pip install gaeh \
		--force-reinstall --no-index --find-links="$(PROJECT_DIR)/dist"

run:
	$(CMD_ACTIVATE_VENV); $(PYTHON) -m src $(FILES)