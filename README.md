# qml2nllphs

Docker used to . . .

## Quickstart
### Build docker
```
$ git clone git@github.com:INGV/qml2nllphs.git
$ cd qml2nllphs
$ docker build --tag qml2nllphs . 
```

### Run docker
to show syntax:
```
$ docker run --rm -v $(pwd)/example:/opt/input qml2nllphs 
```

example:
```
$ docker run --rm -v $(pwd)/example:/opt/input qml2nllphs --qmlin /opt/input/quakeml.xml
```

#### Docker CLI
To override the `ENTRYPOINT` directive and enter into the Docker container, run:
```
$ docker run --rm -it --entrypoint=bash qml2nllphs
```

# Contribute
Please, feel free to contribute.

# Author
(c) 2021 Raffaele Distefano raffaele.distefano[at]ingv.it

(c) 2021 Valentino Lauciani valentino.lauciani[at]ingv.it

Istituto Nazionale di Geofisica e Vulcanologia, Italia
