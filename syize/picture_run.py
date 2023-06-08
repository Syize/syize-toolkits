from syize.picture import *
from syize.string import *
from getopt import getopt, GetoptError
from sys import argv
from typing import Union

from syize.utils import to_file


def print_help(option: str = None):
    if option is not None:
        print(f"Unknown option {option}")
    print("Usage for picture\n\n"
          "Basic options\n"
          "\t-h | --help                            print this message\n"
          "\t-i [filename] | --input [filename]     input picture name\n"
          "\t-o [filename] | --output [filename]    output filename, default is stdout\n\n"
          "Function options\n"
          "\t--ocr                                  extract text from picture\n"
          "\t--ocr-text                             type of text, default is en\n"
          "\t--pdf                                  convert pdf to picture\n"
          "\t--pdf-start [number]                   start page number\n"
          "\t--pdf-end [number]                     end page number\n"
          "\t--pdf-dpi [number]                     picture dpi\n")
    exit(0)


def get_options() -> dict[str, Union[str, int, None]]:
    result = {
        'input': None,
        'output': None,
        'func': None,
        'ocr-text': 'en',
        'pdf-start': None,
        'pdf-end': None,
        'pdf-dpi': 300
    }

    try:
        options, _ = getopt(argv[1:], "hi:o:", ["help", "input=", "output=", "ocr", "ocr-text=", "pdf", "pdf-start=", "pdf-end=", "pdf-dpi="])
        for key, value in options:
            if key in ["-h", "--help"]:
                print_help()
            elif key in ["-i", "--input"]:
                result['input'] = value
            elif key in ["-o", "--output"]:
                result['output'] = value
            elif key in ["--ocr"]:
                result['func'] = "ocr"
            elif key in ["--ocr-text"]:
                result['ocr-text'] = value
            elif key in ["--pdf"]:
                result['func'] = "pdf"
            elif key in ["--pdf-start"]:
                result['pdf-start'] = int(value)
            elif key in ["--pdf-end"]:
                result['pdf-end'] = int(value)
            elif key in ["--pdf-dpi"]:
                result['pdf-dpi'] = int(value)
            else:
                print_help(key)
    except GetoptError:
        print_help()

    # check option
    for key in ['input', 'func']:
        if result[key] is None:
            print_help()

    return result


def run():
    options = get_options()
    if options['func'] == 'ocr':
        res = picture_to_string(options['input'], options['ocr-text'])
        res = remove_redundant_linebreak(res)
        to_file(res, options['output'])
    elif options['func'] == "pdf":
        pdf_to_picture(options['input'], folder_path=options['output'], start=options['pdf-start'], end=options['pdf-end'], dpi=options['pdf-dpi'])
    else:
        raise Exception(f"Unknown option {options['func']}")


__all__ = ['run']


if __name__ == '__main__':
    run()
