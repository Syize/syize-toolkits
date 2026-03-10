"""
syize.fortran
#############

用于数值模式研究的工具。

子模块
******

* :doc:`formatter </api/fortran.formatter>`: 格式化 Fortran 文件中的注释，让其正确的进行缩进，以便 VS Code 正确识别代码块。
* ``palm``: 使用从 PALM 模式中提取的源码以及简单的 wrapper 代码编译得到的 Python 扩展，用于深入研究 PALM 模式中各变量的变化过程。

.. toctree ::
    :maxdepth: 1
    :hidden:

    formatter <fortran.formatter>
"""

from .formatter import *
from .palm import *
