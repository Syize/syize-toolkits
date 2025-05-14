import argparse
from os.path import abspath, exists

import xarray as xr
from rich import print as rich_print

from .utils import logger


def entry_parse_netcdf(args: argparse.Namespace):
    """
    Parse the netcdf and print the info.

    :param args:
    :type args:
    :return:
    :rtype:
    """
    args = vars(args)
    file_path = args["input"]
    file_path = abspath(file_path)

    if not exists(file_path):
        logger.error(f"File not found: {file_path}")
        exit(1)

    try:
        dataset = xr.open_dataset(file_path)
        rich_print("[red]Coordinates in the dataset:[red]")
        rich_print(dataset.coords)
        rich_print("[red]Variables in the dataset:[red]")
        rich_print(dataset.data_vars)

    except ValueError:
        logger.error(f"Can't parse the giving file: {file_path}")
        exit(1)


__all__ = ["entry_parse_netcdf"]
