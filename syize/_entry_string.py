import argparse

from .string import format_string
from .utils import to_file


def entry_format_string(args: argparse.Namespace):
    """
    Entry point for function ``pdf_to_picture``.

    :param args: Parsed args.
    :type args: Namespace
    :return:
    :rtype:
    """
    args_dict = vars(args)
    res = format_string(args_dict["input"])
    to_file(res, args_dict["output"])


__all__ = ["entry_format_string"]
