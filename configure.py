import subprocess, logging, pathlib, os, sys, argparse, shutil
from build.third_party_info import QT_INFO
from build.system import current_os, get_mount_partitions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

PWD = pathlib.Path().absolute()
BUILD_DIR = "build"
BUILD_DIR_WINDOWS = f"{BUILD_DIR}\\windows"

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, errors='ignore')
    result_str = ""
    if result.stdout:
        result_str = result.stdout
    elif result.stderr:
        result_str = result.stderr
    
    logger.info(result_str)
    assert result.returncode == 0, f"Command: {cmd}. Status code: {result.returncode}"
    return result_str, result.returncode


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

class BuildThirdParty:
    def __init__(self, windows_drive_letter = None):
        self.__SCRIPT_BUILD_QT_WINDOWS = f"{BUILD_DIR_WINDOWS}\\build_qt.bat"

        self.python_libs()
        self.qt(windows_drive_letter)

    def python_libs(self):
        run_command("python -m pip install html5lib")

    def qt(self, drive_letter=None):
        """
        Args:
            drive_letter (str | None) - only for Windows.
        """

        logger.info("Starting QT setup...")
        if current_os() == "windows":
            assert drive_letter in get_mount_partitions(), f"Error: the drive letter must be one of these: {get_mount_partitions()}. Got letter: {drive_letter}"

            if not dir_is_exists(f"{drive_letter}:/Qt/{QT_INFO.version}"):
                logger.info("Starting 'configure' QT...")
                run_command(f"{self.__SCRIPT_BUILD_QT_WINDOWS} configure {drive_letter} {QT_INFO.version}")
                logger.info("Starting 'build' QT...")
                run_command(f"{self.__SCRIPT_BUILD_QT_WINDOWS} build {drive_letter}")
                logger.info("Starting 'install' QT...")
                run_command(f"{self.__SCRIPT_BUILD_QT_WINDOWS} install {drive_letter} {QT_INFO.version}")
                logger.info("Starting 'update_env' QT...")
                run_command(f"{self.__SCRIPT_BUILD_QT_WINDOWS} update_env {drive_letter} {QT_INFO.version}")
            else:
                if dir_is_exists(f"{drive_letter}:/Qt/qt-build"):
                    logger.info(f"Delete directory...: {drive_letter}:/Qt/qt-build")
                    remove_path(f"{drive_letter}:/Qt/qt-build")
                
                logger.info(f"Qt is already installed at path: {drive_letter}:\Qt\{QT_INFO.version}")
                logger.info("Starting 'update_env' QT...")
                run_command(f"{self.__SCRIPT_BUILD_QT_WINDOWS} update_env {drive_letter} {QT_INFO.version}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Build Third Party Dependencies.")
    if current_os() == 'windows':
        parser.add_argument('--drive-letter', type=str, required=True, help="Drive letter for Windows OS.")
    
    args = parser.parse_args()

    if current_os() == 'windows':
        drive_letter = args.drive_letter
        BuildThirdParty(drive_letter)
    else:
        logger.info(f"Unsupported OS: {current_os()}")
        exit(1)