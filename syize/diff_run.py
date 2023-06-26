from rich import print as rprint
from os import listdir
from os.path import isdir
from getopt import getopt, GetoptError
from sys import exit, argv
from syize.diff import diff


def help():
    print("Usage for pydiff:\n"
          "\tpydiff [OPTIONS] [FILES]\n"
          "OPTIONS:\n"
          "\t-h | --help                   print this message\n"
          "\t-d | --dir [path]             diff all file in the specific path\n"
          "\n"
          "examples\n"
          "\tpydiff --dir .                diff all file in current path\n"
          "\tpydiff *.dat                  diff all .dat file in current path\n")
    exit(0)


def get_options():
    results = {
        'dir': None,
        'filenames': []
    }

    try:
        options, args = getopt(argv[1:], "hd:", ["help", "dir="])
        for key, value in options:
            if key in ["-h", "--help"]:
                help()
            elif key in ["-d", "--dir"]:
                results['dir'] = value
            else:
                print(f"Unknown parameter: {key}")
        results['filenames'] = args
    except GetoptError:
        help()

    if results['dir'] is not None and len(results['filenames']) > 0:
        rprint("[red]You give a directory path and filename list simultaneously, ignore filenames[red]")
        results['filenames'] = []
    elif results['dir'] is None and len(results['filenames']) == 0:
        help()

    return results


def run():
    options = get_options()
    # print(options)
    # exit(0)
    if options['dir'] is not None:
        # get all file path in this directory
        dir_path = options['dir']
        if dir_path[-1] != '/':
            dir_path += '/'
        filenames = listdir(dir_path)
        filenames = [f"{dir_path}{x}" for x in filenames]
        md5, res = diff(filenames)
    else:
        filenames = options['filenames']
        md5, res = diff(filenames)
    # calculate the percentage
    percent = (len(filenames) - len(res.keys())) * 100 / len(filenames)
    rprint(f"[green]About {percent:.2f}% files are same[green]\n")

    if len(res.keys()) > 0:
        rprint("[red]Below are files which is different and them md5 value:[red]")
        for name in res:
            rprint(f"[red]{name}: {res[name]}[red]")


__all__ = ['run']


if __name__ == '__main__':
    run()
