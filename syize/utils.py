import logging
from typing import Optional

from rich.logging import RichHandler


# init a logger
logger = logging.getLogger("syize")
formatter = logging.Formatter(
    "%(name)s :: %(message)s", datefmt="%m-%d %H:%M:%S")
# use rich handler
handler = RichHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def to_file(contents: str, filename: Optional[str] = None):
    """
    Write the contents to a file.

    :param contents:
    :type contents:
    :param filename:
    :type filename:
    """
    if filename is None:
        print(contents)
    else:
        with open(filename, 'w') as f:
            f.write(contents)


__all__ = ['to_file', "logger"]
