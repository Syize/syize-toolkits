import argparse

from .picture import pdf_to_picture, picture_to_string
from .string import remove_redundant_linebreak
from .utils import to_file


def entry_picture_to_string(args: argparse.Namespace):
    """
    Entry point for function ``picture_to_string``.

    :param args: Parsed args.
    :type args: Namespace
    :return:
    :rtype:
    """
    args_dict = vars(args)
    res = picture_to_string(args_dict["input"], args_dict["text"])
    res = remove_redundant_linebreak(res)
    to_file(res, args_dict["output"])


def entry_pdf_to_picture(args: argparse.Namespace):
    """
    Entry point for function ``pdf_to_picture``.

    :param args: Parsed args.
    :type args: Namespace
    :return:
    :rtype:
    """
    args_dict = vars(args)
    pdf_to_picture(args_dict["input"], folder_path=args_dict["output"], start=args_dict["start"], end=args_dict["end"], dpi=args_dict["dpi"])


__all__ = ["entry_picture_to_string", "entry_pdf_to_picture"]
