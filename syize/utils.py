from rich.progress import TextColumn, BarColumn, TimeRemainingColumn, Progress
from rich.logging import RichHandler
import logging


download_progress = Progress(
    TextColumn("[red]{task.description}"),
    BarColumn(bar_width=None),
    "•", TimeRemainingColumn()
)


logger = logging.getLogger("syize toolkits")
formatter = logging.Formatter("%(name)s :: %(message)s", datefmt="%m-%d %H:%M:%S")
handler = RichHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def to_file(contents: str, filename: str):
    if filename is None:
        print(contents)
    else:
        with open(filename, 'a') as f:
            f.write(contents)


__all__ = ['to_file', 'download_progress', 'logger']
