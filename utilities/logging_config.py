import logging
import os


def configure_logging():
    """
    Configures the logging settings for the application.

    Returns:
        logging.Logger: The configured logger object.
    """
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logs_dir = os.path.join(script_dir, "logs")
    os.makedirs(
        logs_dir, exist_ok=True
    )  # Create the 'logs' directory if it doesn't exist
    file_path = os.path.join(logs_dir, "error.log")

    # Create a file handler
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.ERROR)

    # Create a formatter and add it to the file handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger
