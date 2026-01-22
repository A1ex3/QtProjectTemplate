import subprocess, pathlib, os, argparse, shutil, tarfile, socket, urllib.request, urllib.parse
from scripts.third_party_info import ThirdPartyInfo, EnumThirdPartyInfoType
from scripts.system import current_os, get_mount_partitions, EnumPlatformSystem
from scripts.update_qt_version import QT_VERSION

PWD = pathlib.Path().absolute()
SCRIPTS_DIR = "scripts"

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
        self.__THIRD_PARTY_DIR = "third_party"
        self.__SCRIPTS_WINDOWS_DIR = f"{SCRIPTS_DIR}\\windows"
        self.__SCRIPTS_LINUX_DIR = f"{SCRIPTS_DIR}/linux"

        self.qt(windows_drive_letter)

    def qt(self, drive_letter=None):
        """
        Args:
            drive_letter (str | None) - only for Windows.
        """

        QT_NAME = "Qt"

        SCRIPT_BUILD_QT_WINDOWS = f"{self.__SCRIPTS_WINDOWS_DIR}\\build_qt.bat"
        SCRIPT_BUILD_QT_LINUX = f"{self.__SCRIPTS_LINUX_DIR}/build_qt.sh"

        def qt_mirror_ping(mirrors_list):
            for mirror in mirrors_list:
                if ping(urllib.parse.urlparse(mirror.url).netloc):
                    return mirror
            raise RuntimeError(f"All Qt mirrors is unavailable: {mirrors_list}")

        QT_MIRROR_YANDEX = "https://mirror.yandex.ru/mirrors/qt.io/official_releases/qt"
        QT_MIRROR_YANDEX_MINOR_VERSION = QT_VERSION.rsplit('.', 1)[0]
        QT_MIRROR_YANDEX_ARCHIVE = f"qt-everywhere-src-{QT_VERSION}.tar.xz"
        QT_MIRROR_YANDEX_URL = f"{QT_MIRROR_YANDEX}/{QT_MIRROR_YANDEX_MINOR_VERSION}/{QT_VERSION}/single/{QT_MIRROR_YANDEX_ARCHIVE}"

        # In order of priority.
        QT_MIRRORS_THIRD_PARTY_INFO_NAME_ORIGINAL_REPO = f"{QT_NAME}_OriginalRepo"
        QT_MIRRORS_THIRD_PARTY_INFO_NAME_YANDEX_MIRROR = f"{QT_NAME}_YandexMirror"
        QT_MIRRORS = [
            ThirdPartyInfo(
                struct_type=EnumThirdPartyInfoType.GIT,
                name=QT_MIRRORS_THIRD_PARTY_INFO_NAME_ORIGINAL_REPO,
                version=QT_VERSION,
                hash_commit="077347cc6d198053fb61cc0841c5c0c60a7deeb1",
                url="https://code.qt.io/qt/qt5.git"
            ),
            ThirdPartyInfo(
                struct_type=EnumThirdPartyInfoType.HTTP_FILE,
                name=QT_MIRRORS_THIRD_PARTY_INFO_NAME_YANDEX_MIRROR,
                version=QT_VERSION,
                url=QT_MIRROR_YANDEX_URL
            )
        ]

        def qt_mirror_make_download_path():
            path_str_ = f"{self.__THIRD_PARTY_DIR}"
            if QT_MIRROR_INFO.name == QT_MIRRORS_THIRD_PARTY_INFO_NAME_YANDEX_MIRROR:
                return f"{path_str_}/{QT_MIRROR_YANDEX_ARCHIVE}"
            else:
                raise RuntimeError(f"Unknown Qt mirror name: {QT_MIRROR_INFO.name}")

        print("Starting Qt setup...")
        if current_os() == EnumPlatformSystem.WINDOWS:
            assert drive_letter in get_mount_partitions(), f"Error: the drive letter must be one of these: {get_mount_partitions()}. Got letter: {drive_letter}"

            if not dir_is_exists(f"{drive_letter}:/Qt/{QT_VERSION}"):
                if not dir_is_exists(f"{self.__THIRD_PARTY_DIR}/qt"):
                    QT_MIRROR_INFO = qt_mirror_ping(QT_MIRRORS)

                    if QT_MIRROR_INFO.struct_type == EnumThirdPartyInfoType.HTTP_FILE:
                        QT_MIRROR_DOWNLOAD_PATH = qt_mirror_make_download_path()

                        download_file(QT_MIRROR_INFO.url, QT_MIRROR_DOWNLOAD_PATH)
                        extract_tar_xz(f"{self.__THIRD_PARTY_DIR}/qt", QT_MIRROR_DOWNLOAD_PATH)
                        remove_path(QT_MIRROR_DOWNLOAD_PATH)
                    elif QT_MIRROR_INFO.struct_type == EnumThirdPartyInfoType.GIT:
                        print("Qt sources not found. Cloning...")
                        run_command(f"git clone {QT_MIRROR_INFO.url} {self.__THIRD_PARTY_DIR}/qt")
                        os.chdir(f"{self.__THIRD_PARTY_DIR}/qt")
                        run_command(f"git checkout {QT_MIRROR_INFO.hash_commit}")
                        run_command(f"git submodule update --init --recursive --depth=1 qtbase qtdeclarative qtshadertools qtimageformats qtsvg qttranslations qttools")
                        os.chdir(PWD)

                print("Starting 'configure' Qt...")
                run_command(f"{SCRIPT_BUILD_QT_WINDOWS} configure {drive_letter} {QT_VERSION}")
                print("Starting 'build' Qt...")
                run_command(f"{SCRIPT_BUILD_QT_WINDOWS} build {drive_letter}")
                print("Starting 'install' Qt...")
                run_command(f"{SCRIPT_BUILD_QT_WINDOWS} install {drive_letter} {QT_VERSION}")
                print("Starting 'update_env' Qt...")
                run_command(f"{SCRIPT_BUILD_QT_WINDOWS} update_env {drive_letter} {QT_VERSION}")

                if dir_is_exists(f"{drive_letter}:/Qt/qt-build"):
                    print(f"Delete directory...: {drive_letter}:/Qt/qt-build")
                    remove_path(f"{drive_letter}:/Qt/qt-build")
            else:
                print(f"Qt is already installed at path: {drive_letter}:/Qt/{QT_VERSION}")

                if dir_is_exists(f"{drive_letter}:/Qt/qt-build"):
                    print(f"Delete directory...: {drive_letter}:/Qt/qt-build")
                    remove_path(f"{drive_letter}:/Qt/qt-build")
                
                print("Starting 'update_env' Qt...")
                run_command(f"{SCRIPT_BUILD_QT_WINDOWS} update_env {drive_letter} {QT_VERSION}")
        
        if current_os() == EnumPlatformSystem.LINUX:
            if not dir_is_exists(f"/usr/lib/Qt/{QT_VERSION}"):
                if not dir_is_exists(f"{self.__THIRD_PARTY_DIR}/qt"):
                    QT_MIRROR_INFO = qt_mirror_ping(QT_MIRRORS)

                    if QT_MIRROR_INFO.struct_type == EnumThirdPartyInfoType.HTTP_FILE:
                        QT_MIRROR_DOWNLOAD_PATH = qt_mirror_make_download_path()

                        download_file(QT_MIRROR_INFO.url, QT_MIRROR_DOWNLOAD_PATH)
                        extract_tar_xz(f"{self.__THIRD_PARTY_DIR}/qt", QT_MIRROR_DOWNLOAD_PATH)
                        run_command(f"chown -R $USER:$USER {self.__THIRD_PARTY_DIR}/qt")
                        run_command(f"chmod -R 755 {self.__THIRD_PARTY_DIR}/qt")
                        remove_path(QT_MIRROR_DOWNLOAD_PATH)
                    elif QT_MIRROR_INFO.struct_type == EnumThirdPartyInfoType.GIT:
                        print("Qt sources not found. Cloning...")
                        run_command(f"git clone {QT_MIRROR_INFO.url} {self.__THIRD_PARTY_DIR}/qt")
                        os.chdir(f"{self.__THIRD_PARTY_DIR}/qt")
                        run_command(f"git checkout {QT_MIRROR_INFO.hash_commit}")
                        run_command(f"git submodule update --init --recursive --depth=1 qtbase qtdeclarative qtshadertools qtimageformats qtsvg qttranslations qttools")
                        os.chdir(PWD)

                print("Starting 'configure' Qt...")
                run_command(f"{SCRIPT_BUILD_QT_LINUX} configure {QT_VERSION}")
                print("Starting 'build' Qt...")
                run_command(f"{SCRIPT_BUILD_QT_LINUX} build")
                print("Starting 'install' Qt...")
                run_command(f"{SCRIPT_BUILD_QT_LINUX} install {QT_VERSION}")
                print("Starting 'update_env' Qt...")
                run_command(f"{SCRIPT_BUILD_QT_LINUX} update_env {QT_VERSION}")

                if dir_is_exists("/tmp/Qt/qt-build"):
                    print("Delete directory...: /tmp/Qt")
                    remove_path("/tmp/Qt")
            else:
                print(f"Qt is already installed at path: /usr/lib/Qt/{QT_VERSION}")

                if dir_is_exists("/tmp/Qt/qt-build"):
                    print("Delete directory...: /tmp/Qt")
                    remove_path("/tmp/Qt")

                print("Starting 'update_env' Qt...")
                run_command(f"{SCRIPT_BUILD_QT_LINUX} update_env {QT_VERSION}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Build Third Party Dependencies.")
    if current_os() == EnumPlatformSystem.WINDOWS:
        parser.add_argument('--drive-letter', type=str, required=True, help="Drive letter for Windows OS.")
    
    args = parser.parse_args()

    if current_os() == EnumPlatformSystem.WINDOWS:
        drive_letter = args.drive_letter
        PrepareThirdParty(windows_drive_letter=drive_letter)
    elif current_os() == EnumPlatformSystem.LINUX:
        PrepareThirdParty()
    else:
        print(f"Unsupported OS: {current_os().NAME}")
        exit(1)