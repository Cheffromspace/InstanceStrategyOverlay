import logging


def configure_logging():
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    # Create a file handler
    file_handler = logging.FileHandler("error.log")
    file_handler.setLevel(logging.ERROR)

    # Create a formatter and add it to the file handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger
