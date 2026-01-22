QT_VERSION = "6.10.0"

if __name__ == "__main__":
    import re

    def read_file(filename):
        with open(filename, mode="r", encoding='utf-8') as f:
            return f.read()

    def write_file(filename, data):
        with open(filename, mode="w", encoding='utf-8') as f:
            f.write(data)

    DOCKERFILE_LINUX_PATH = "scripts/linux/Dockerfile"
    DOCKERFILE_LINUX_STR = read_file(DOCKERFILE_LINUX_PATH)
    DOCKERFILE_LINUX_STR = re.sub(
        r"(/usr/lib/Qt/)[\d.]+(/lib/cmake/Qt6)",
        rf"\g<1>{QT_VERSION}\g<2>",
        DOCKERFILE_LINUX_STR
    )
    write_file(DOCKERFILE_LINUX_PATH, DOCKERFILE_LINUX_STR)