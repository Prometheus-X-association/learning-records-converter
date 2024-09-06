from random import choice


def random_case_in_string(text: str) -> str:
    """Randomly change char case in string
    xapi > xApI or XAPI or xAPi

    Args:
        text (str): string to modify

    Returns:
        str: modified string. If text passed is empty, return text
    """
    if text:
        return "".join(choice((str.upper, str.lower))(char) for char in str(text))
    else:
        return text
