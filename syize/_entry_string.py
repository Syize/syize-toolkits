import argparse

from .string import *
from .utils import *


def entry_format_string(args: argparse.Namespace):
    """
    Entry point for function ``pdf_to_picture``.

    :param args: Parsed args.
    :type args: Namespace
    :return:
    :rtype:
    """
    args = vars(args)
    res = format_string(args["input"])
    to_file(res, args["output"])


__all__ = ["entry_format_string"]
