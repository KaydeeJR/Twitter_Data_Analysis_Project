import logging
import sys
import os

def logger_console_config(logger_name):
    """
    Create logger with the specified name. Output all log levels. Attach logger to console.

    Parameter:
            logger_name -> the name of the logger
    """
    logger = logging.getLogger(logger_name)
    logFormatter = logging.Formatter(fmt="%(asctime)s: %(levelname)s: %(message)s")
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(logFormatter)
    logger.addHandler(console)
    return logger

def logger_file_config(dir_path, logger_name, file_name):
    """
    Create logger with the specified name. Set up logger to output logs to file in current directory.
    Output all log levels.
    
    Parameters:
                dir_path -> folder to save log file
                logger_name -> name of logger object
                file_name -> file to store logs (.log)
    """
    logger = logging.getLogger(logger_name)
    logFormatter = logging.Formatter(fmt="%(asctime)s: %(levelname)s: %(message)s")
    fileHandler = logging.FileHandler(filename=dir_path+'\\'+file_name, mode='a')
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)
    return logger