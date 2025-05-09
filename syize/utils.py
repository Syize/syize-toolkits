import logging
from typing import Optional

from rich.logging import RichHandler


logger = logging.getLogger("wrfrun")
formatter = logging.Formatter("%(name)s :: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
# use rich handler
handler = RichHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def to_file(contents: str, filename: Optional[str] = None):
    """
    Print the contents to stdout or write contents to a file.

    :param contents: Strings.
    :type contents: str
    :param filename: File path.
    :type filename: str
    :return:
    :rtype:
    """
    if filename is None:
        print(contents)
    else:
        with open(filename, 'w') as f:
            f.write(contents)


__all__ = ['to_file', "logger"]
