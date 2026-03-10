"""
syize.tv_show_manager.utils
###########################

初始化 ``tvsm`` 专用的 logger。
"""

import logging

from rich.logging import RichHandler

logger = logging.getLogger("tvsm")
formatter = logging.Formatter("%(name)s :: %(message)s", datefmt="%m-%d %H:%M:%S")
# use rich handler
handler = RichHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


__all__ = ["logger"]
