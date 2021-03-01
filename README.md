[![License](https://img.shields.io/github/license/INGV/qml2nllphs.svg)](https://github.com/INGV/qml2nllphs/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/INGV/qml2nllphs.svg)](https://github.com/INGV/qml2nllphs/issues)

![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/ingv/qml2nllphs)
![Docker Image Size (latest semver)](https://img.shields.io/docker/image-size/ingv/qml2nllphs?sort=semver)
![Docker Pulls](https://img.shields.io/docker/pulls/ingv/qml2nllphs)

# qml2nllphs [![Version](https://img.shields.io/badge/dynamic/yaml?label=ver&query=softwareVersion&url=https://raw.githubusercontent.com/INGV/qml2nllphs/master/publiccode.yml)](https://github.com/INGV/qml2nllphs/blob/master/publiccode.yml) [![CircleCI](https://circleci.com/gh/INGV/qml2nllphs/tree/master.svg?style=svg)](https://circleci.com/gh/INGV/qml2nllphs/tree/master)

Docker used to . . .

## Quickstart
### Docker image
To obtain *qml2nllphs* docker image, you have two options:

#### 1) Get built image from DockerHub (*preferred*)
Get the last built image from DockerHub repository:
```
$ docker pull ingv/qml2nllphs
```

#### 2) Build by yourself
First, clone the git repository
```
$ git clone https://github.com/INGV/qml2nllphs.git
$ cd qml2nllphs
$ docker build --tag ingv/qml2nllphs .
```

in case of errors, try:
```
$ docker build --no-cache --pull --tag ingv/qml2nllphs .
```

### Run docker
To run the container, use the command below; the `-v` option is used to "mount" working directory into container:
```
$ docker run --rm --user $(id -u):$(id -g) -v $(pwd)/example:/opt/input ingv/qml2nllphs
```

example:
```
$ docker run --rm --user $(id -u):$(id -g) -v $(pwd)/example:/opt/input ingv/qml2nllphs --qmlin /opt/input/quakeml.xml
```

#### Docker CLI
To override the `ENTRYPOINT` directive and enter into the Docker container, run:
```
$ docker run --rm -it --user $(id -u):$(id -g) --entrypoint=bash qml2nllphs
```

## Update Docker image from DockerHub
Get last Docker image from DockerHub repository:
```
$ docker pull ingv/qml2nllphs
```

# Contribute
Please, feel free to contribute.

# Author
(c) 2021 Raffaele Distefano raffaele.distefano[at]ingv.it

(c) 2021 Valentino Lauciani valentino.lauciani[at]ingv.it

Istituto Nazionale di Geofisica e Vulcanologia, Italia
