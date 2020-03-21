FROM debian:stable

# meta data
LABEL maintainer="Fabian Jankowski"
LABEL description="Docker image for MeerTRAP Trigger Tools."

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    gfortran \
    git \
    make \
    netcat \
    net-tools \
    procps \
    python3 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    vim \
 && rm -rf /var/lib/apt/lists/*

# add smart history search
RUN echo "\"\e[A\":history-search-backward" >> /etc/skel/.inputrc && \
    echo "\"\e[B\":history-search-forward" >> /etc/skel/.inputrc

# python packages
RUN pip3 install --upgrade pip

RUN pip3 install \
    astropy \
    ipython \
    numpy \
    pybind11 \
    pytz \
    pyyaml

# install pygedm later, as it requires numpy's f2py
RUN pip3 install pygedm

# 4piskytools
RUN pip3 install git+https://github.com/timstaley/fourpiskytools.git@master

# mosaic for beam calculations
#RUN pip3 install git+https://gitlab.mpifr-bonn.mpg.de/wchen/Beamforming.git@master
RUN git clone https://gitlab.mpifr-bonn.mpg.de/wchen/Beamforming.git /software/mosaic

# install our software in docker image
ARG SOFT_PATH="/software/meertrig"

RUN mkdir -p ${SOFT_PATH}
COPY . ${SOFT_PATH}

ENV PYTHONPATH ${SOFT_PATH}:${PYTHONPATH}
WORKDIR ${SOFT_PATH}
