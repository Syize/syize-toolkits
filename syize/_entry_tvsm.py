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
    args = vars(args)
    feature_str = args["feature_str"]
    season_num = args["season"]
    start = args["start"]
    end = args["end"]
    sort_episode(feature_str, season_num, start, end)


def entry_rename_episode_file(args: argparse.Namespace):
    """
    Entry point for function ``rename_episode_file``.

    :param args: Parsed args.
    :type args: Namespace.
    :return:
    :rtype:
    """
    args = vars(args)
    prefix = args["prefix"]
    force = args["force"]
    rename_episode_file(prefix, force)


__all__ = ["entry_rename_episode_file", "entry_sort_episode"]
