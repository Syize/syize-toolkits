from os import listdir, makedirs, chdir, getcwd
from os.path import exists
from shutil import move

from .rename import rename_episode_file
from .utils import logger

FEATURE_STRING_TUPLE = ("%d", "%0d", "%HQH", "%HSJ", "%HSF", "%LS", "%HSX")

FEATURE_STRING_MAP = {
    "%HQH": ["前", "後"],
    "%HSJ": ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"],
    "%HSF": ["壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖", "拾"],
    "%LS": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"],
    "%HSX": ["上", "下"],
}


def sort_episode(feature_str="第%HSJ章", season_num=1, start=1, end=10):
    """Manage the shows automatically.

    :param feature_str: Feature string that will be used to find the episode number, defaults to "第%HSJ章".
    :type feature_str: str, optional
    :param season_num: Number of season.
    :type season_num: int
    :param start: If ``feature_str`` has ``"%d"``, this will be used to generate episode number, defaults to 1.
    :type start: int, optional
    :param end: If ``feature_str`` has ``"%d"``, this will be used to generate episode number, defaults to 10.
    :type end: int, optional
    """
    # check feature string
    if "%" in feature_str:
        feature_string = ""
        for _str in FEATURE_STRING_TUPLE:
            if _str in feature_str:
                logger.info(f"Find feature string: {_str}")
                feature_string = _str
                break

        if feature_string == "":
            logger.info(f"Feature string not found, assume you don't give any feature string.")
            logger.info(f"Use string '{feature_str}' to find the episode.")
            feature_string = feature_str
            normal_string = True

        else:
            normal_string = False

    else:
        logger.info(f"Use string '{feature_str}' to find the episode.")
        feature_string = feature_str
        normal_string = True

    if normal_string:
        feature_string_list = [feature_string]

    else:
        if feature_string == "%d":
            feature_string_list = [feature_str.replace(feature_string, f"{x}") for x in range(start, end)]
        elif feature_string == "%0d":
            feature_string_list = [feature_str.replace(feature_string, f"{str(x).rjust(2, '0')}") for x in range(start, end)]
        else:
            feature_string_list = [feature_str.replace(feature_string, f"{x}") for x in FEATURE_STRING_MAP[feature_string]]

    file_list = listdir()
    season_string = str(season_num).rjust(2, "0")
    season_path = f"Season {season_string}"
    episode_index = start
    root_path = getcwd()
    if not exists(season_path):
        makedirs(season_path)

    for _feature_string in feature_string_list:
        _file_list = [x for x in file_list if _feature_string in x and not x.endswith((".jpg", ".png", ".nfo", ".trickplay"))]

        if len(_file_list) > 0:
            prefix_str = "Episode S{SEASON}E{EPISODE}".format(SEASON=season_string, EPISODE=f"{episode_index}".rjust(2, "0"))
            logger.info(f"Found files for {prefix_str}: {_file_list}")
            work_path = f"{season_path}/{prefix_str}"

            if not exists(work_path):
                makedirs(work_path)

            for _file in _file_list:
                if exists(f"{work_path}/{_file}"):
                    logger.error(f"File '{_file}' exists in '{work_path}', please check it.")
                    exit(1)
                move(_file, f"{work_path}/{_file}")

            chdir(work_path)
            rename_episode_file(prefix_str)
            chdir(root_path)

        episode_index += 1

        if episode_index > end:
            exit(0)


__all__ = ["sort_episode"]
