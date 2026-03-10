"""
syize.tv_show_manage.rename
###########################

用于对媒体库文件进行重命名的工具。

.. autosummary::
    :toctree: generated/

    rename_episode_file
"""

from os import listdir
from os.path import exists
from shutil import move

from .utils import logger


def rename_episode_file(prefix: str, force=False):
    """
    This function collects all files in one episode and renames them.

    :param prefix: Prefix string, should be in "Episode SXXEXX" format, in which "XX" means the number of the season and episode.
    :type prefix: str
    :param force: If true, force to rename the file even the target file exists.
    :type force: bool
    :return:
    :rtype:
    """
    if len(prefix) == 0:
        logger.error("The `prefix` must not be empty")
        exit(1)

    valid_characters = set("1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM ")
    prefix_characters = set(prefix)

    if len(prefix_characters - (prefix_characters & valid_characters)) > 0:
        logger.error(
            "Found invalid character in the `prefix`. The `prefix` must only contain white space, numbers and alphabets."
        )
        exit(1)

    file_list = listdir()
    file_postfix_list = [x.split(".")[-1] for x in file_list]

    new_file_list = [f"{prefix}.{x}" for x in file_postfix_list]

    for old_file, new_file in zip(file_list, new_file_list):
        if exists(new_file):
            if force:
                logger.warning(f"File exists: {new_file}, overwrite it because you have set `force=True`")
            else:
                logger.error(f"File exists: {new_file}, stop renaming")
                exit(1)

        move(old_file, new_file)


__all__ = ["rename_episode_file"]
