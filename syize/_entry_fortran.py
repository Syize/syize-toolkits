import argparse
from os.path import abspath, exists

from .fortran import CommentFormatter
from .utils import logger


def entry_parse_fortran(args: argparse.Namespace):
    """
    Process Fortran code.
    """
    args_dict = vars(args)
    file_path = args_dict["input"]
    is_in_place = args_dict.get("replace", False)
    out_file = args_dict.get("output")
    
    file_path = abspath(file_path)

    if not exists(file_path):
        logger.error(f"File not found: {file_path}")
        exit(1)
        
    CommentFormatter(out_file=out_file, in_place=is_in_place).format(file_path)


__all__ = ["entry_parse_fortran"]
