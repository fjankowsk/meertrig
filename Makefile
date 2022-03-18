BLK         =   black
DCK         =   docker
PIP         =   pip

BASEDIR     =   $(CURDIR)
SRCDIR      =   ${BASEDIR}/meertrig
DOCKERFILE  =   ${BASEDIR}/docker/Dockerfile

help:
	@echo 'Makefile for MeerTRAP Trigger Tools'
	@echo 'Usage:'
	@echo 'make black           reformat the code using black code formatter'
	@echo 'make clean           remove temporary files'
	@echo 'make install         install the module locally'
	@echo 'make production      build docker image for production use'
	@echo 'make interactive     run an interactive shell'

black:
	${BLK} *.py */*.py */*/*.py

clean:
	rm -f ${SRCDIR}/*.pyc
	rm -rf ${BASEDIR}/build
	rm -rf ${BASEDIR}/dist
	rm -rf ${BASEDIR}/meertrig.egg-info

install:
	${PIP} install .

interactive:
	${DCK} run -it --rm --network=host \
	meertrig bash

production:
	${DCK} build \
	--file ${DOCKERFILE} \
	--tag meertrig ${BASEDIR}

.PHONY: help black clean install interactive production