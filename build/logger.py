import logging, os

class Logger:
    def __init__(self, level, log_to_console=False, path_to_log_file=None, using_in_python=False, path_to_executable_file=None):
        """
        Args:
            level (_Level) - log level
            log_to_console (bool)
            path_to_log_file (str)
            using_in_python (bool) - must be `True` if the logger is called in a python script
            path_to_execute_file (str) - use 'True' if you want to call the logger outside of the python script
        """
        self.__level = level
        self.__path_to_log_file = path_to_log_file
        self.__log_to_console = log_to_console
        self.__using_in_python = using_in_python
        self.__path_to_executable_file = path_to_executable_file
        self.__logger = logging.getLogger()

        self.__init()

    def __ensure_log_file_exists(self, path_to_log_file):
        """
        Ensure that the log file and its directories exist. 
        If the file or directories do not exist, they will be created.

        Args:
            path_to_log_file (str): the full path to the log file.
        """
        log_dir = os.path.dirname(path_to_log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if not os.path.exists(path_to_log_file):
            with open(path_to_log_file, 'w', encoding='utf-8'):
                pass

    def __init(self):
        self.__logger.setLevel(self.__level)

        if self.__logger.hasHandlers():
            self.__logger.handlers.clear()

        if self.__using_in_python:
            formatter = logging.Formatter('%(pathname)s:%(lineno)d - %(funcName)s - %(asctime)s - %(levelname)s - %(message)s')
        else:
            formatter = logging.Formatter(f'{self.__path_to_executable_file} - %(asctime)s - %(levelname)s - %(message)s')

        if self.__path_to_log_file:
            self.__ensure_log_file_exists(self.__path_to_log_file)

            file_handler = logging.FileHandler(self.__path_to_log_file, mode='a', encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.__logger.addHandler(file_handler)

        if self.__log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.__logger.addHandler(console_handler)

    def get_logger(self):
        return self.__logger

class LoggerBuilder:
    def __init__(self):
        self.__level = logging.INFO
        self.__log_to_console = False
        self.__using_in_python = False
        self.__path_to_log_file = None
        self.__path_to_executable_file = None

    def set_level(self, level):
        self.__level = level
        return self

    def enable_console_logging(self):
        self.__log_to_console = True
        return self

    def set_file_path(self, value):
        self.__path_to_log_file = value
        return self
    
    def set_executable_file_path(self, value):
        self.__path_to_executable_file = value
        return self

    def set_using_in_python(self, value):
        self.__using_in_python = value
        return self

    def build(self):
        return Logger(self.__level, self.__log_to_console, self.__path_to_log_file, self.__using_in_python, self.__path_to_executable_file).get_logger()
    
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--log_file_path', type=str, required=True, help="Preferably use the full path.")
    parser.add_argument('--executable_file_path', type=str, required=True, help="Use the full path to the file where the logger is called.")
    parser.add_argument('--log_msg_level', type=str, required=True, help="Levels: info, warning, error, critical")
    parser.add_argument('--log_msg', type=str, required=True, help="Log message.")
    args = parser.parse_args()

    log_file_path = args.log_file_path
    executable_file_path = args.executable_file_path
    log_msg_level = args.log_msg_level
    log_msg_level = log_msg_level.lower()
    log_msg = args.log_msg

    logger = LoggerBuilder() \
        .set_level(logging.INFO) \
        .set_file_path(log_file_path) \
        .set_executable_file_path(executable_file_path) \
        .build()
    
    if log_msg_level == "info":
        logger.info(log_msg)
    elif log_msg_level == "warning":
        logger.warning(log_msg)
    elif log_msg_level == "error":
        logger.warning(log_msg)
    elif log_msg_level == "critical":
        logger.warning(log_msg)
    else:
        Exception("Unknown logging level!")
        exit(1)