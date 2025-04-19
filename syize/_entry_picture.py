import argparse

from .picture import *
from .string import *
from .utils import to_file


def entry_picture_to_string(args: argparse.Namespace):
    """
    Entry point for function ``picture_to_string``.

    :param args: Parsed args.
    :type args: Namespace
    :return:
    :rtype:
    """
    args = vars(args)
    res = picture_to_string(args["input"], args["text"])
    res = remove_redundant_linebreak(res)
    to_file(res, args["output"])


def entry_pdf_to_picture(args: argparse.Namespace):
    """
    Entry point for function ``pdf_to_picture``.

    :param args: Parsed args.
    :type args: Namespace
    :return:
    :rtype:
    """
    args = vars(args)
    pdf_to_picture(args["input"], folder_path=args["output"], start=args["start"], end=args["end"], dpi=args["dpi"])


__all__ = ["entry_picture_to_string", "entry_pdf_to_picture"]
