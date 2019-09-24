PY?         =   python
DCK	    	=   docker

BASEDIR     =   $(CURDIR)
SRCDIR      =   ${BASEDIR}/meertrig
DOCKERFILE  =   ${BASEDIR}/docker/Dockerfile

help:
	@echo 'Makefile for MeerTRAP Trigger Tools'
	@echo 'Usage:'
	@echo 'make clean           remove temporary files'
	@echo 'make production      build docker image for production use'
	@echo 'make interactive     run an interactive shell'

clean:
	rm -f ${SRCDIR}/*.pyc
	rm -rf ${BASEDIR}/build
	rm -rf ${BASEDIR}/dist
	rm -rf ${BASEDIR}/meertrig.egg-info

interactive:
	${DCK} run -it --rm --network=host \
	meertrig bash

production:
	${DCK} build \
	--file ${DOCKERFILE} \
	--tag meertrig ${BASEDIR}

.PHONY: help clean interactive production