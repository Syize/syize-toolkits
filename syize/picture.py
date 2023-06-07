from pytesseract import image_to_string
from PIL import Image
from os.path import exists


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


__all__ = ['picture_to_string']
