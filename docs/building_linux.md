# Build instructions for Linux (Docker)

## Requirements:
- Docker

## Clone source code.
```bash
git clone https://github.com/A1ex3/QtProjectTemplate.git
```

## Building a Docker image.
```bash
docker build -t qtproject:latest -f build/linux/Dockerfile .
```

## Building the project.
```bash
docker run --rm -it -v "$PWD:/usr/qtproject" qtproject:latest
```