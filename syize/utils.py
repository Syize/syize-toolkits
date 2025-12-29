import argparse
import logging
from os import listdir
from os.path import isdir
from typing import Optional

from rich.logging import RichHandler

# init a logger
logger = logging.getLogger("syize")
formatter = logging.Formatter("%(name)s :: %(message)s", datefmt="%m-%d %H:%M:%S")
# use rich handler
handler = RichHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


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


def list_meson_files(args: argparse.Namespace):
    files = listdir()
    files = [x for x in files if not isdir(x)]
    files.sort()

    for _file in files:
        print(f'"{_file}",')


__all__ = ['to_file', "logger", "list_meson_files"]
