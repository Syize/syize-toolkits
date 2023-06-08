from pytesseract import image_to_string
from PIL import Image
from os.path import exists
from os import makedirs
from pdf2image import convert_from_path
from rich import print as rprint


lang_dict = {
    'cn': 'sim',
    'en': 'eng'
}


def picture_to_string(picture_path: str, text_type='cn') -> str:
    """
    extract text from a picture
    :param picture_path:
    :param text_type:
    :return:
    """
    # check picture
    assert exists(picture_path), "Picture doesn't exist"
    # check text type
    assert text_type in ['cn', 'en'], f"Unknown text type: {text_type}, supported type: ['cn, 'en']"

    image = Image.open(picture_path)
    lang = lang_dict[text_type]
    string = image_to_string(image, lang=lang)

    return string


def pdf_to_picture(file_path: str, folder_path: str = './', start: int = None, end: int = None, dpi: int = None):
    """
    convert pdf to image
    :param file_path:
    :param folder_path: default is ./
    :param start:
    :param end:
    :param dpi:
    :return:
    """
    if folder_path is None:
        folder_path = "./"
    if not exists(folder_path):
        makedirs(folder_path)
    rprint(f"[red]Converting to image and saving to {folder_path} ...[red]")
    return convert_from_path(file_path, output_folder=folder_path, fmt='png', first_page=start, last_page=end, dpi=dpi)


__all__ = ['picture_to_string', 'pdf_to_picture']
