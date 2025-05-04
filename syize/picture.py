from os import makedirs
from os.path import exists

from PIL import Image
from pdf2image import convert_from_path
from pytesseract import image_to_string
from rich import print as rprint

lang_dict = {
    'cn': 'chi_sim',
    'en': 'eng'
}


def picture_to_string(picture_path: str, text_type='cn') -> str:
    """
    Extract text from a picture.

    :param picture_path: Picture path.
    :param text_type: Text language. Valid key: ``["cn", "en"]``.
    :return:
    """
    assert exists(picture_path), "Picture doesn't exist"
    assert text_type in ['cn', 'en'], f"Unknown text type: {text_type}, supported type: ['cn, 'en']"

    image = Image.open(picture_path)
    lang = lang_dict[text_type]
    string = image_to_string(image, lang=lang)

    if text_type == "cn":
        # remove redundant white blank
        string = "".join(string.split(" "))
        # replace comma
        string = string.replace(",", "，")

    return string


def pdf_to_picture(file_path: str, folder_path: str = './', start: int = None, end: int = None, dpi: int = None):
    """
    Convert a PDF file to images.

    :param file_path: PDF file path.
    :param folder_path: Directory to store images.
    :param start: Start page number.
    :param end: End page number.
    :param dpi: Image DPI.
    :return:
    """
    if folder_path is None:
        folder_path = "./"
    if not exists(folder_path):
        makedirs(folder_path)
    rprint(f"[red]Converting to image and saving to {folder_path} ...[red]")
    return convert_from_path(file_path, output_folder=folder_path, fmt='png', first_page=start, last_page=end, dpi=dpi)


__all__ = ['picture_to_string', 'pdf_to_picture']
