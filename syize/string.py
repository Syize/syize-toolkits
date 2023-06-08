def remove_redundant_linebreak(string: str) -> str:
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


__all__ = ['remove_redundant_linebreak']
