from os import makedirs
from os.path import exists
from requests import get
from typing import TypedDict, Optional

from PySide6.QtCore import QObject, Signal, Slot

from ..utils import logger


class DownloadParams(TypedDict):
    """
    Download parameters.
    """
    url: str
    headers: dict
    proxy: Optional[dict]
    filename: str
    save_path: str


class Downloader(QObject):
    """
    Backend downloader.
    """

    SignalDownloadFinish = Signal(bool)

    def __init__(self):
        super().__init__()

    # ######################### Slot Functions #########################
    @Slot(DownloadParams)
    def slot_download_file(self, params: DownloadParams):
        """
        Download a file.

        :return:
        :rtype:
        """
        url = params["url"]
        headers = params["headers"]
        proxy = params["proxy"]
        filename = params["filename"]
        save_path = params["save_path"]

        if not exists(save_path):
            makedirs(save_path)

        response = get(url, headers=headers, proxies=proxy)

        if response.status_code != 200:
            logger.warning(f"Download failed. Status code: {response.status_code}.")
            self.SignalDownloadFinish.emit(False)
            return

        with open(f"{save_path}/{filename}", "wb") as f:
            f.write(response.content)

        self.SignalDownloadFinish.emit(True)


__all__ = ["DownloadParams", "Downloader"]
