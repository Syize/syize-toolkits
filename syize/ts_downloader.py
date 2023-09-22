from syize.utils import download_progress, logger
from requests import get
from traceback import format_exc
from typing import Dict


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "",
    "DNT": "1",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}


def download_ts(m3u8_path: str, save_path="output.ts", headers: Dict[str, str] = None, init_url: str = None):
    """
    download *.ts file and concat them from Internet
    :param m3u8_path: a m3u8 file download url or local path
    :param save_path: output file save path. Default is `./output.ts` file
    :param headers: custom headers. if is `None`, use default headers
    :param init_url: sometimes urls in .m3u8 file don't contain init url, you can give me it by this params.
    :return:
    """
    # check headers
    if headers is None:
        logger.warn(f"You are using default headers. If you fail to download files, try to set custom headers")
    else:
        # check if there is any key like `:XXXXX` in headers
        for key in headers:
            if key.startswith(":"):
                logger.warn(f"Invalid header found: {key}. While requests doesn't support headers start with \":\", I'll remove the \":\" in it."
                            f"This could lead to download failure")
                headers[key[1:]] = headers[key]
                headers.pop(key)
    logger.info(f"The download headers is {headers}")

    # check if m3u8 is an url or local file
    if m3u8_path.startswith("http"):
        # try to download m3u8 file
        logger.info(f"Trying to download m3u8 list from {m3u8_path}")
        try:
            res = get(m3u8_path, headers=headers)
            if res.status_code == 200:
                m3u8 = res.text
            else:
                logger.error(f"Fail to download m3u8 file: status code {res.status_code}, exit")
                exit(1)
        except KeyboardInterrupt:
            logger.debug(f"Stop by user")
            exit(1)
        except:
            logger.error(f"Error occurred: {format_exc()}")
            exit(0)
    else:
        with open(m3u8_path, "r") as f:
            m3u8 = f.read()

    # get file list
    ts_file_list = [x for x in m3u8.split("\n") if x.endswith(".ts")]
    # get init url
    if ts_file_list[0].startswith("http"):
        # no need to add init url
        init_url = None
    elif not m3u8.startswith("http"):
        if init_url is None:
            logger.error(f"The .ts file url in m3u8 is like {ts_file_list[0]}, but we need a init url to download. Give me by `init_url` params")
            exit(1)
    else:
        init_url = "/".join(m3u8_path.split("/")[:3])
    # generate download url list
    url_list = [f"{init_url}/{x}" if init_url is not None else x for x in ts_file_list]

    # download
    with open(save_path, "ab") as output:
        with download_progress:
            pid = download_progress.add_task("Downloading...", total=len(url_list))

            for url in url_list:
                # we will try up to 5 times
                retry_num = 0
                while True:
                    try:
                        res = get(url, headers=headers)
                        if res.status_code == 200:
                            output.write(res.content)
                            break
                    except KeyboardInterrupt:
                        logger.debug(f"Stop by user")
                        exit(1)
                    except:
                        logger.debug(f"Error occurred: {format_exc()}")
                        pass

                    if retry_num >= 4:
                        # fail to download
                        logger.error(f"I have tried 5 times and still can't download, exit")
                        exit(1)
                    retry_num += 1

                download_progress.update(pid, advance=1)
