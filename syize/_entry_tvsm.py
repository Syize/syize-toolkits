import argparse

from .tv_show_manage import rename_episode_file, sort_episode


def entry_sort_episode(args: argparse.Namespace):
    """
    Entry point for function ``sort_episode``.

    :param args: Parsed args.
    :type args: Namespace.
    :return:
    :rtype:
    """
    args_dict = vars(args)
    feature_str = args_dict["feature_str"]
    season_num = args_dict["season"]
    start = args_dict["start"]
    end = args_dict["end"]
    sort_episode(feature_str, season_num, start, end)


def entry_rename_episode_file(args: argparse.Namespace):
    """
    Entry point for function ``rename_episode_file``.

    :param args: Parsed args.
    :type args: Namespace.
    :return:
    :rtype:
    """
    args_dict = vars(args)
    prefix = args_dict["prefix"]
    force = args_dict["force"]
    rename_episode_file(prefix, force)


__all__ = ["entry_rename_episode_file", "entry_sort_episode"]
