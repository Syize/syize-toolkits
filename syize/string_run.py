from syize.string import *
from syize.utils import *
from sys import argv
from getopt import getopt, GetoptError


def print_help(option: str = None):
    if option is not None:
        print(f"Unknown option {option}")
    print("Usage for string\n\n"
          "Basic options\n"
          "\t-h | --help                            print this message\n"
          "\t-i [input] | --input [input]           input picture name\n"
          "\t-o [filename] | --output [filename]    output filename, default is stdout\n\n"
          "Function options\n"
          "\t--format                               format string, remove redundant line break\n")
    exit(0)
    
    
def get_options() -> dict[str, str]:
    result = {
        'input': None,
        'output': None,
        'func': None
    }

    try:
        options, _ = getopt(argv[1:], "hi:o:", ["help", "input=", "output=", "format"])
        for key, value in options:
            if key in ["-h", "--help"]:
                print_help()
            elif key in ["-i", "--input"]:
                result['input'] = value
            elif key in ["-o", "--output"]:
                result['output'] = value
            elif key in ["--format"]:
                result['func'] = "format"
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
    if options['func'] == 'format':
        res = remove_redundant_linebreak(options['input'])
        to_file(res, options['output'])
    else:
        raise Exception(f"Unknown option {options['func']}")


__all__ = ['run']


if __name__ == '__main__':
    run()
