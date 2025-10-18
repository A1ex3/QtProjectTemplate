import subprocess, pathlib, os, argparse, shutil, tarfile, socket, urllib.request, urllib.parse
from build.third_party_info import QT_INFO
from build.system import current_os, get_mount_partitions

PWD = pathlib.Path().absolute()
BUILD_DIR = "build"
BUILD_DIR_WINDOWS = f"{BUILD_DIR}\\windows"
BUILD_DIR_LINUX = f"{BUILD_DIR}/linux"

def run_command(cmd):
    print(cmd)

    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors='ignore')

    stdout_data = result.stdout
    stderr_data = result.stderr

    if stdout_data:
        print(stdout_data)
    if stderr_data:
        print(stderr_data)
    
    assert result.returncode == 0, f"Command: {cmd}. Status code: {result.returncode}"
    
    return result.returncode

def dir_is_exists(path):
    if os.path.isdir(path):
        result = next(os.scandir(path), None)
        return True if result is not None else False
    else:
        return False

def remove_path(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        return

def extract_tar_xz(dest, src):
    with tarfile.open(src, 'r:xz') as tar:
        root_dir = tar.getnames()[0].split('/')[0]
        for member in tar.getmembers():
            member_path = os.path.join(dest, os.path.relpath(member.name, root_dir))
            if member.isdir():
                os.makedirs(member_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(member_path), exist_ok=True)
                with open(member_path, 'wb') as f:
                    f.write(tar.extractfile(member).read())

def ping(host, port=443, timeout=15):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def download_file(url, dest):
    dest_path = pathlib.Path(dest)
    if dest_path.exists():
        print(f"{dest} already exists, skipping download.")
        return
    print(f"Downloading {url} -> {dest} ...")
    urllib.request.urlretrieve(url, dest)
    print("Download completed.")

class PrepareThirdParty:
    def __init__(self, windows_drive_letter = None):
        self.__SCRIPT_BUILD_QT_WINDOWS = f"{BUILD_DIR_WINDOWS}\\build_qt.bat"
        self.__SCRIPT_BUILD_QT_LINUX = f"{BUILD_DIR_LINUX}/build_qt.sh"

        self.qt(windows_drive_letter)

    def qt(self, drive_letter=None):
        """
        Args:
            drive_letter (str | None) - only for Windows.
        """

        QT_MIRROR = "https://mirror.yandex.ru/mirrors/qt.io/official_releases/qt"
        QT_MINOR_VERSION = QT_INFO.version.rsplit('.', 1)[0]
        QT_MIRROR_ARCHIVE = f"qt-everywhere-src-{QT_INFO.version}.tar.xz"
        QT_MIRROR_DOWNLOAD_PATH = f"third_party/{QT_MIRROR_ARCHIVE}"
        QT_MIRROR_URL = f"{QT_MIRROR}/{QT_MINOR_VERSION}/{QT_INFO.version}/single/{QT_MIRROR_ARCHIVE}"

        print("Starting Qt setup...")

        # Check git host
        main_git_host = urllib.parse.urlparse(QT_INFO.repository).netloc
        if not ping(main_git_host):
            print(f"Git server {main_git_host} is not reachable, mirror will be used instead.")
            use_mirror = True
        else:
            use_mirror = False

        if current_os() == "windows":
            assert drive_letter in get_mount_partitions(), f"Error: the drive letter must be one of these: {get_mount_partitions()}. Got letter: {drive_letter}"

            if not dir_is_exists(f"{drive_letter}:/Qt/{QT_INFO.version}"):
                if not dir_is_exists("third_party/qt"):
                    if use_mirror:
                        download_file(QT_MIRROR_URL, QT_MIRROR_DOWNLOAD_PATH)
                        extract_tar_xz("third_party/qt", QT_MIRROR_DOWNLOAD_PATH)
                        remove_path(QT_MIRROR_DOWNLOAD_PATH)
                    else:
                        print("Qt sources not found. Cloning...")
                        run_command(f"git clone {QT_INFO.repository} third_party/qt")
                        os.chdir("third_party/qt")
                        run_command(f"git checkout {QT_INFO.hash_commit}")
                        run_command(f"git submodule update --init --recursive --depth=1 qtbase qtdeclarative qtshadertools qtimageformats qtsvg qttranslations qttools")
                        os.chdir(PWD)

                print("Starting 'configure' Qt...")
                run_command(f"{self.__SCRIPT_BUILD_QT_WINDOWS} configure {drive_letter} {QT_INFO.version}")
                print("Starting 'build' Qt...")
                run_command(f"{self.__SCRIPT_BUILD_QT_WINDOWS} build {drive_letter}")
                print("Starting 'install' Qt...")
                run_command(f"{self.__SCRIPT_BUILD_QT_WINDOWS} install {drive_letter} {QT_INFO.version}")
                print("Starting 'update_env' Qt...")
                run_command(f"{self.__SCRIPT_BUILD_QT_WINDOWS} update_env {drive_letter} {QT_INFO.version}")

                if dir_is_exists(f"{drive_letter}:/Qt/qt-build"):
                    print(f"Delete directory...: {drive_letter}:/Qt/qt-build")
                    remove_path(f"{drive_letter}:/Qt/qt-build")
            else:
                print(f"Qt is already installed at path: {drive_letter}:/Qt/{QT_INFO.version}")

                if dir_is_exists(f"{drive_letter}:/Qt/qt-build"):
                    print(f"Delete directory...: {drive_letter}:/Qt/qt-build")
                    remove_path(f"{drive_letter}:/Qt/qt-build")
                
                print("Starting 'update_env' Qt...")
                run_command(f"{self.__SCRIPT_BUILD_QT_WINDOWS} update_env {drive_letter} {QT_INFO.version}")
        
        if current_os() == "linux":
            if not dir_is_exists(f"/usr/lib/Qt/{QT_INFO.version}"):
                if not dir_is_exists("third_party/qt"):
                    if use_mirror:
                        download_file(QT_MIRROR_URL, QT_MIRROR_DOWNLOAD_PATH)
                        extract_tar_xz("third_party/qt", QT_MIRROR_DOWNLOAD_PATH)
                        run_command("chown -R $USER:$USER third_party/qt")
                        run_command("chmod -R 755 third_party/qt")
                        remove_path(QT_MIRROR_DOWNLOAD_PATH)
                    else:
                        print("Qt sources not found. Cloning...")
                        run_command(f"git clone {QT_INFO.repository} third_party/qt")
                        os.chdir("third_party/qt")
                        run_command(f"git checkout {QT_INFO.hash_commit}")
                        run_command(f"git submodule update --init --recursive --depth=1 qtbase qtdeclarative qtshadertools qtimageformats qtsvg qttranslations qttools")
                        os.chdir(PWD)

                print("Starting 'configure' Qt...")
                run_command(f"{self.__SCRIPT_BUILD_QT_LINUX} configure {QT_INFO.version}")
                print("Starting 'build' Qt...")
                run_command(f"{self.__SCRIPT_BUILD_QT_LINUX} build")
                print("Starting 'install' Qt...")
                run_command(f"{self.__SCRIPT_BUILD_QT_LINUX} install {QT_INFO.version}")
                print("Starting 'update_env' Qt...")
                run_command(f"{self.__SCRIPT_BUILD_QT_LINUX} update_env {QT_INFO.version}")

                if dir_is_exists("/tmp/Qt/qt-build"):
                    print("Delete directory...: /tmp/Qt")
                    remove_path("/tmp/Qt")
            else:
                print(f"Qt is already installed at path: /usr/lib/Qt/{QT_INFO.version}")

                if dir_is_exists("/tmp/Qt/qt-build"):
                    print("Delete directory...: /tmp/Qt")
                    remove_path("/tmp/Qt")

                print("Starting 'update_env' Qt...")
                run_command(f"{self.__SCRIPT_BUILD_QT_LINUX} update_env {QT_INFO.version}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Build Third Party Dependencies.")
    if current_os() == 'windows':
        parser.add_argument('--drive-letter', type=str, required=True, help="Drive letter for Windows OS.")
    
    args = parser.parse_args()

    if current_os() == 'windows':
        drive_letter = args.drive_letter
        PrepareThirdParty(drive_letter)
    elif current_os() == 'linux':
        PrepareThirdParty()
    else:
        print(f"Unsupported OS: {current_os()}")
        exit(1)