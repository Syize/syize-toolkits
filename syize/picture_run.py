from syize.picture import *
from getopt import getopt, GetoptError
from sys import argv


def print_help(option: str = None):
    if option is not None:
        print(f"Unknown option {option}")
    print("Usage for picture.py\n\n"
          "Basic options\n"
          "\t-h | --help                            print this message\n"
          "\t-i [filename] | --input [filename]     input picture name\n"
          "\t-o [filename] | --output [filename]    output filename, default is stdout\n\n"
          "Function options\n"
          "\t--ocr                                  extract text from picture\n"
          "\t--ocr-text                             type of text, default is en\n")
    exit(0)


def get_options() -> dict[str, str]:
    result = {
        'input': None,
        'output': None,
        'func': None,
        'ocr-text': 'en'
    }

    try:
        options, _ = getopt(argv[1:], "hi:o:", ["print_help=", "input=", "output=", "ocr", "ocr-text="])
        for key, value in options:
            if key in ["-h", "--print_help"]:
                print_help()
            elif key in ["-i", "--input"]:
                result['input'] = value
            elif key in ["-o", "--output"]:
                result['output'] = value
            elif key in ["--ocr"]:
                result['func'] = "ocr"
            elif key in ["--ocr-text"]:
                result['ocr-text'] = value
            else:
                print_help(key)
    except GetoptError:
        print_help()

    # check option
    for key in ['input', 'func']:
        if result[key] is None:
            print_help()

    return result


def to_file(contents: str, filename: str):
    if filename is None:
        print(contents)
    else:
        with open(filename, 'w') as f:
            f.write(contents)


def run():
    options = get_options()
    if options['func'] == 'ocr':
        res = picture_to_string(options['input'], options['ocr-text'])
        to_file(res, options['output'])
    else:
        raise Exception(f"Unknown option {options['func']}")


__all__ = ['run']


if __name__ == '__main__':
    run()
