def to_file(contents: str, filename: str):
    if filename is None:
        print(contents)
    else:
        with open(filename, 'a') as f:
            f.write(contents)


__all__ = ['to_file']
