from syize.ts_downloader import download_ts
from getopt import getopt, GetoptError
from sys import argv
from typing import Dict, Union
from json import loads


def print_help():
    print("Usage for ts_downloader\n\n"
          "\t-h | --help                                 show this message\n"
          "\t-m [url or path] | --m3u8 [url or path]     m3u8 download url or local file path\n"
          "\t-o [path] | --output [path]                 output filename\n"
          "\t-H [str or path] | --headers [str or path]  headers string or a json file\n"
          "\t-i [url] | --init-url [url]                 init url")
    exit(0)


def get_options() -> Dict[str, Union[str, None]]:
    result = {
        "m3u8": None,
        "output": "output.ts",
        "headers": None,
        "init_url": None
    }

    try:
        options, _ = getopt(argv[1:], "hm:o:H:i:", ["help", "m3u8=", "output=", "headers=", "init-url="])
        for key, value in options:
            if key in ["-h", "--help"]:
                print_help()
            elif key in ["-m", "--m3u8"]:
                result["m3u8"] = value
            elif key in ["-o", "--output"]:
                result["output"] = value
            elif key in ["-H", "--headers"]:
                result["headers"] = value
            elif key in ["-i", "--init-url"]:
                result["init_url"] = value
            else:
                print_help()
    except GetoptError:
        print_help()

    # check option
    for key in ["m3u8", "output"]:
        if result[key] is None:
            print_help()

    # parse headers
    if result["headers"] is not None:
        # parse directly
        if result["headers"].startswith('{'):
            result["headers"] = loads(result["headers"])
        else:
            with open(result["headers"], "r") as f:
                result["headers"] = loads(f.read())

    return result


def run():
    options = get_options()
    download_ts(options["m3u8"], options["output"], options["headers"], options["init_url"])


if __name__ == "__main__":
    run()
