import logging
from os.path import basename, dirname
from shutil import move

LOGGER = logging.getLogger("syize")


class CommentFormatter:
    """
    Class to format comments in Fortran.
    """
    def __init__(self, out_file: None | str = None, in_place=False) -> None:
        """
        You have to give either ``out_file`` or ``in_place=True``.

        **Usage**

        1. Format the comment and save to new file.

        >>> from syize.fortran import CommentFormatter
        >>> in_file = "./example.f90"
        >>> out_file = "./example_new.f90"
        >>> CommentFormatter(out_file=out_file).format(in_file)

        2. Save changes in-place.

        >>> from syize.fortran import CommentFormatter
        >>> in_file = "./example.f90"
        >>> CommentFormatter(in_place=True).format(in_file)

        :param out_file: Output file path, defaults to None
        :type out_file: None | str, optional
        :param in_place: If save changes to the original file, defaults to False
        :type in_place: bool, optional
        """
        if in_place:
            self._is_in_place = in_place
            # will be set latter
            self._out_file = ""
        elif out_file is not None:
            self._is_in_place = False
            self._out_file = out_file

        else:
            LOGGER.error("You have to either set [magenta]in_place[/] or give out file path.")
            exit(1)
        
        self._buffer_list: list[str] = []
        self._buffer = ""
        self._indent = 0

        self._is_inspecting_indentation = False
    
    def format(self, file_path: str):
        """
        Format the comment in ``file_path``. 

        :param file_path: Input file path.
        :type file_path: str
        """
        in_file = open(file_path, "r")

        for _line in in_file:
            # comment
            if _line.startswith("!"):
                if _line.strip("!\n").strip() == "":
                    pass
                else:
                    self._buffer_list.append(_line)

                    # start inspecting indentation length
                    self._is_inspecting_indentation = True

            # empty line
            elif _line == "\n":
                self._buffer += _line

            # code
            else:
                valid_word = _line.split()[0]
                indentation = _line.split(valid_word)[0]
                self._indent = len(indentation)

                if self._is_inspecting_indentation:
                    self.write_buffer()
                    self._is_inspecting_indentation = False

                self._buffer += _line

        in_file.close()

        if self._is_in_place:
            self._out_file = f"{dirname(file_path)}/.{basename(file_path)}.tmp"

        with open(self._out_file, "w") as f:
            f.write(self._buffer)

        if self._is_in_place:
            move(self._out_file, file_path)
            LOGGER.info("Formatted code saved to the original file.")

        else:
            LOGGER.info(f"Formatted code saved to: '{self._out_file}'")

    def write_buffer(self):
        """
        Flush the buffer.
        """
        for _buffer in self._buffer_list:
            # check original indentation
            _indentation = len(_buffer.split("!")[0])

            if _indentation >= self._indent:
                self._buffer += _buffer

            else:
                self._buffer += "".rjust(self._indent - _indentation) + _buffer

        self._buffer_list = []


__all__ = ["CommentFormatter"]
            