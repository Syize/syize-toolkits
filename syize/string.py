from os.path import exists


def remove_redundant_linebreak(string: str) -> str:
    """
    Remove line break in the giving string.

    :param string:
    :type string:
    :return:
    :rtype:
    """
    # split by '\n'
    string_list = string.split('\n')
    # print(string_list)
    res = []
    for words in string_list:
        # if is '', replace it with '\n'
        if words == '':
            if len(res) > 0:
                res[-1] = res[-1][:-1]
            res.append('\n')
        elif words[0].isupper() and (len(res) > 0 and res[-1] != '\n' and res[-1][-2] == '.'):
            res.append('\n')
            res.append(words)
        else:
            res.append(words + ' ')

    res = ''.join(res)

    return res


def format_string(input_str: str) -> str:
    """
    Format the giving string.

    :param input_str: Input string or a file path.
    :type input_str: str
    :return:
    :rtype:
    """
    if exists(input_str):
        with open(input_str, "r") as f:
            input_str = f.read()

    res = remove_redundant_linebreak(input_str)
    return res


__all__ = ['remove_redundant_linebreak', "format_string"]
