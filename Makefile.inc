#
# invitae-hw-variant-search/Makefile.inc ---
#

# Usage: include ./Makefile.inc

ifeq (${INVITAE_VS_DIR},)
  $(error source ./setup.env)
endif

__include_default:
	@echo "Makefile.inc: The first target should be before 'Makefile.inc'."
	exit 1

SHELL:=/bin/bash
.SUFFIXES:

#####

#: the system python used to build the VE
sys_python3_exe=$(shell PATH=/usr/local/bin:/usr/bin:${PATH} type -p python3)

#: the python in our VE.
python_cmd:=${INVITAE_VS_VE_DIR}/bin/python3

pip3_cmd:=${python_cmd} -m pip

unittest_cmd:=${python_cmd} -m unittest

#####

git_cmd:=git
git_version_cmd:=${git_cmd} describe --always --dirty --long --tags

#####

# defaults
autopep8_files ?= $(wildcard *.py)

autopep8_cmd:=autopep8 \
	  --aggressive \
	  --in-place \
	  --max-line-length 120

_autopep8:
	${autopep8_cmd} ${autopep8_files}

isort_cmd:=isort \
	  --multi-line 3 \
	  --trailing-comma \
	  --line-width 1

_isort:
	${isort_cmd} ${autopep8_files}

pylint_cmd:=pylint --py3k

_pylint:
	${pylint_cmd} ${autopep8_files}

#####

psql_cmd:=psql -v ON_ERROR_STOP=1

#####

_delete_backup_files:
	find . \( -name \*~ -o -name \*.pyc \) -print -delete
