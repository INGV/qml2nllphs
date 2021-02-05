FROM debian:buster-slim

LABEL maintainer="Raffaele Di Stefano <raffaele.distefano@ingv.it>"
ENV DEBIAN_FRONTEND=noninteractive 

# Installing all needed applications
RUN apt-get clean \
    && apt-get update \
    && apt-get dist-upgrade -y --no-install-recommends \
    && apt-get install -y \
        python3 \
        python3-pip \
        gcc \
        build-essential \
        systemd \
        wget \
        zip \
        vim

# Adding python3 libraries
RUN python3 -m pip install numpy
RUN python3 -m pip install obspy

# Copy files
COPY qml2nllphs.py /opt
COPY entrypoint.sh /opt

#
RUN echo "export MPLCONFIGDIR=/tmp" >> ~/.bashrc
RUN echo "alias ll='ls -l' >> ~/.bashrc

#
WORKDIR /opt
ENTRYPOINT ["bash", "/opt/entrypoint.sh"]
