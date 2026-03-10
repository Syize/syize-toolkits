"""
syize.tv_show_manage
####################

用于管理媒体库的工具。

Submodules
**********

=========================================== ======================================
:doc:`rename </api/tv_show_manage.rename>`  用于对媒体库文件进行重命名的工具。
:doc:`sort </api/tv_show_manage.sort>`      用于对媒体库文件进行排序并重命名的工具。
:doc:`utils </api/tv_show_manage.utils>`    初始化 ``tvsm`` 专用的 logger。
=========================================== ======================================

.. toctree::
    :maxdepth: 1
    :hidden:

    rename <tv_show_manage.rename>
    sort <tv_show_manage.sort>
    utils <tv_show_manage.utils>
"""

from .rename import *
from .sort import *
