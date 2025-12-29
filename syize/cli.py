import argparse
import sys

from ._entry_netcdf import *
from ._entry_picture import *
from ._entry_string import *
from ._entry_tvsm import *
from .utils import list_meson_files


def entry_point():
    """
    Command line entry point.

    :return:
    :rtype:
    """
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-l", "--list", action="store_true", help="List all files in current directory.")
    args_parser.set_defaults(func=list_meson_files)
    
    subparsers = args_parser.add_subparsers(title="Subcommands", description="Valid subcommands", help="Subcommands help.")

    ocr_parser = subparsers.add_parser("ocr", help="Extract texts from a picture.")
    ocr_parser.add_argument("-i", "--input", type=str, help="Input path of the picture.", required=True)
    ocr_parser.add_argument("-o", "--output", type=str, default=None, help="Output file path. Default is stdout.")
    ocr_parser.add_argument("-t", "--text", type=str, default="en", help="Language code of the text.")
    ocr_parser.set_defaults(func=entry_picture_to_string)

    pdf_parser = subparsers.add_parser("pdf", help="Extract pictures from a PDF.")
    pdf_parser.add_argument("-i", "--input", type=str, help="Input path of the PDF.", required=True)
    pdf_parser.add_argument("-o", "--output", type=str, default="./", help="Output directory path. Default is './'.")
    pdf_parser.add_argument("-s", "--start", type=int, default=None, help="Start page number.")
    pdf_parser.add_argument("-e", "--end", type=int, default=None, help="End page number.")
    pdf_parser.add_argument("-d", "--dpi", type=int, default=200, help="DPI of the picture.")
    pdf_parser.set_defaults(func=entry_pdf_to_picture)

    str_parser = subparsers.add_parser("str", help="Process the giving string.")
    str_parser.add_argument("-i", "--input", type=str, help="Input string or a file.", required=True)
    str_parser.add_argument("-o", "--output", type=str, default=None, help="Output file path. Default is stdout.")
    str_parser.set_defaults(func=entry_format_string)

    netcdf_parser = subparsers.add_parser("nc", help="Parse a netcdf file and print its info.")
    netcdf_parser.add_argument("-i", "--input", type=str, help="Input file.", required=True)
    netcdf_parser.set_defaults(func=entry_parse_netcdf)

    args = args_parser.parse_args(args=None if sys.argv[1:] else ["--help"])
    args.func(args)


def tvsm_entry_point():
    """
    tvsm command line entry point.

    :return:
    :rtype:
    """
    args_parser = argparse.ArgumentParser()
    subparsers = args_parser.add_subparsers(title="Subcommands", description="Valid subcommands", help="Subcommands help.")

    sort_parser = subparsers.add_parser("sort", help="Identify episode files and sort them.")
    sort_parser.add_argument(
        "feature_str", type=str,
        help="Feature strings help tvsm identify episode numbers. Should contain one of these strings: [%%HQH, %%d, %%0d, %%HSJ, %%HSF, %%LS].",
        # required=True
    )
    sort_parser.add_argument("-S", "--season", type=int, default=1, help="Season number.")
    sort_parser.add_argument("-s", "--start", type=int, default=1, help="Start number of the episode.")
    sort_parser.add_argument("-e", "--end", type=int, default=10, help="End number of the episode.")
    sort_parser.set_defaults(func=entry_sort_episode)

    rename_parser = subparsers.add_parser("rename", help="Rename episode files.")
    rename_parser.add_argument("prefix", type=str, help="Prefix of the new file name. For example, 'Episode S01E01'.")
    rename_parser.add_argument("-f", "--force", action="store_true", help="Overwrite existed files. BE CAREFUL.")
    rename_parser.set_defaults(func=entry_rename_episode_file)

    args = args_parser.parse_args(args=None if sys.argv[1:] else ["--help"])
    args.func(args)


__all__ = ["entry_point", "tvsm_entry_point"]
