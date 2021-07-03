#
# invitae-hw-variant-search/Makefile ---
#

_default: _test

include ./Makefile.inc

#####

_apt_get_install:
	sudo apt-get install \
	  python3-venv

_brew_install:
	brew install \
	  python

#####

# do we have a python3?
ifeq (${sys_python3_exe},)
  $(error "sys_python3_exe wasnt found.")
endif

_ve_build:
	mkdir -p "$(dir ${INVITAE_VS_VE_DIR})"
#
	${sys_python3_exe} -m venv "${INVITAE_VS_VE_DIR}"
#
	${pip3_cmd} install --upgrade pip
	${pip3_cmd} install --upgrade autopep8 isort pylint
#
	${pip3_cmd} install -e ./src/invitae-vs-core
	${pip3_cmd} install -e ./src/invitae-vs-server

_ve_rm:
	-rm -rf "${INVITAE_VS_VE_DIR}"

_ve_rebuild: _ve_rm _ve_build

${INVITAE_VS_VE_DIR}:
	make _ve_rebuild

_ve_exists: ${INVITAE_VS_VE_DIR}

#####

#
autopep8_files+=$(wildcard ./src/*/setup.py)
autopep8_files+=$(wildcard ./src/*/*/*.py)

_precommit+=_ve_rebuild
_precommit+=_isort
_precommit+=_autopep8
_precommit+=_pylint
_precommit+=_test

_precommit: ${_precommit}

#####

${INVITAE_VS_DATA_TSV}:
	cd $(dir ${INVITAE_VS_DATA_TSV}) && unzip ${@}.zip

_data_tsv: ${INVITAE_VS_DATA_TSV}

#####

_db_rm_sqlite_file:
	-rm -f ${INVITAE_VS_SQLITE_FILE}

_db_data_load:
#
	make _db_rm_sqlite_file
#
	invitae-vs-core \
	  --db-create-tables \
	  --db-data-load "${INVITAE_VS_DATA_TSV}"
#
	wc -l "${INVITAE_VS_DATA_TSV}"
#
	sqlite3 "${INVITAE_VS_SQLITE_FILE}" \
	  "select count(*) from variant;"

#####

_test_help:
	invitae-vs-core --help

# Suggest the first chars
_test_gene_autocomplete_first:
	invitae-vs-core \
	 --gene-autocomplete ""

_test_gene_autocomplete_AX:
	invitae-vs-core \
	 --gene-autocomplete "AX"

# shouldnt have any more
_test_gene_autocomplete_AXIN2:
	invitae-vs-core \
	 --gene-autocomplete "AXIN2"

_test_gene_autocomplete_doesnotexist:
	invitae-vs-core \
	 --gene-autocomplete "doesnotexist"

_test_gene_autocomplete+=_test_gene_autocomplete_first
_test_gene_autocomplete+=_test_gene_autocomplete_AX
_test_gene_autocomplete+=_test_gene_autocomplete_AXIN2
_test_gene_autocomplete+=_test_gene_autocomplete_doesnotexist

_test_gene_autocomplete: ${_test_gene_autocomplete}

#####

_test_query_1:
	invitae-vs-core \
	 --q-gene-like "AP%" \
	 --q-limit 10

_test_query_2:
	invitae-vs-core \
	 --q-genomic-start '112136000:112136999'

#####

_server_run_flask:
	flask run \
	  --host ${INVITAE_VS_SERVER_BIND} \
	  --port ${INVITAE_VS_SERVER_PORT}

_server_run_gunicorn:
	./bin/invitae-vs-server

#####

_docker_build:
	cd ./docker && make ${@}

_deploy_server:
	cd ./ansible && make ${@}

#####

# prereq
_test+=_ve_exists
_test+=_data_tsv
_test+=_test_help

# load data
_test+=_db_rm_sqlite_file
_test+=_db_data_load
#
_test+=_test_gene_autocomplete
#
_test+=_test_query_1
_test+=_test_query_2

_test: ${_test}
