import hashlib


def diff(filenames: list[str, ...]) -> tuple[str, dict[str, str]]:
    """
    calculate the md5 of multiple file names and return different files with their md5
    :param filenames: filename list
    :return: dict[filename, md5]
    """
    # read file content and calculate md5
    md5_lists = []

    for name in filenames:
        with open(name, 'r') as f:
            md5_lists.append(hashlib.md5(f.read().encode('utf-8')).hexdigest())

    # calculate the number of each md5
    md5_dict = {}
    for md5 in md5_lists:
        if md5 in md5_dict:
            md5_dict[md5] += 1
        else:
            md5_dict[md5] = 0

    # find the most md5
    most_number = max(md5_dict.values())
    for item in md5_dict.items():
        if most_number == item[1]:
            most_md5 = item[0]
    md5_dict.pop(most_md5)

    res = {name: md5 for (name, md5) in zip(filenames, md5_lists) if md5 != most_md5}

    return most_md5, res


__all__ = ['diff']
