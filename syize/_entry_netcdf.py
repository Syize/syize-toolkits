import argparse
from os.path import abspath, exists

from .nc import NCView
from .utils import logger


def entry_parse_netcdf(args: argparse.Namespace):
    """
    Parse the netcdf and print the info.

    :param args:
    :type args:
    :return:
    :rtype:
    """
    args_dict = vars(args)
    file_path = args_dict["input"]
    file_path = abspath(file_path)

    if not exists(file_path):
        logger.error(f"File not found: {file_path}")
        exit(1)

    try:
        NCView(file_path).interact()

    except ValueError:
        logger.error(f"Can't parse the giving file: {file_path}")
        exit(1)

    except KeyboardInterrupt:
        exit(0)


__all__ = ["entry_parse_netcdf"]
