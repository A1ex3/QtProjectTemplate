# Build instructions for Linux (Docker)

## Requirements:
- Docker

## Clone source code.
```bash
git clone https://github.com/A1ex3/QtProjectTemplate.git
```

## Building a Docker image.
```bash
docker build -t qtproject:latest -f scripts/linux/Dockerfile .
```

## Building the project.
```bash
docker run --rm -it -v "$PWD:/home/user/project" qtproject:latest
```

## Building inside the container.

### Prepare the environment and configure the project
```bash
source /etc/profile
```

```bash
cmake -B out -G Ninja .
```

### Build
```bash
cmake --build out --config Release
```