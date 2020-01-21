import io, re
import pandas as pd
from bs4 import BeautifulSoup
from pdfminer.converter import HTMLConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pprint import pprint

patterns = {
    '/Users/programming/PycharmProjects/crime/datasets/OK/Codebooks/2013.pdf':
        "^(\\n)*(?P<desc>.+)(?P<sep>{sep})(?P<var>{var})",
    }


def clean_text(text: str, sep = ':'):
    text = str(text)
    text = ' '.join(text.split())
    for s in sep:
        text = text.replace(s, '')
    text = text.strip()
    return text


def get_soup(codebook_path: str):
    resource_manager = PDFResourceManager()
    file_handle      = io.StringIO()
    converter        = HTMLConverter(resource_manager, file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(codebook_path, 'rb') as file:
        for page in PDFPage.get_pages(file):
            page_interpreter.process_page(page)
        text = file_handle.getvalue()

    converter.close()
    file.close()

    if text:
        soup = BeautifulSoup(text, features='html.parser')
        return soup


def get_pattern(codebook_path: str, variable: str, sep = ':', default_pattern = r"^.*(?P<var>{var})(?P<sep>{sep})(?P<desc>.+)"):
    """
    Parameters
    ----------
    codebook_path : str
        Path to an existing codebook pdf.

    variable : str
        Identifier/variable in the codebook.

    sep : str or iterable of str
        Separator/delimiter(s) that separates the `variable` from its description in the codebook.
        If an element of sep is a reserved character in regex (e.g. a character in "+*?^$.[]{}()|/"), then
        it needs to be escaped with a backslash in order to represent a literal character.

    default_pattern : str
        A string that compiles to a regex pattern.
        Must define "(?P<var>{var})" and "(?P<sep>{sep})" as named capture groups.
        Must define "(?P<desc>)" as well, although what it matches is up to you.

    Returns
    -------
    str
        A regex pattern with `variable` and `sep` substituted in.
        Contains named capture groups "(?P<var>)", "(?P<sep>)", and "(?P<desc>)"
    """

    if len(sep) > 1 and not isinstance(sep, str):
        sep = '|'.join(sep)

    default_pattern = default_pattern.format(var=variable, sep=sep)
    pattern = patterns.get(codebook_path, default_pattern)
    return re.compile(pattern, flags=re.I)


def extract_codebook(codebook_path, variables, sep = ':', default_pattern = r"^.*(?P<var>{var})(?P<sep>{sep})(?P<desc>.+)"):
    codebook_dict = {}

    try:
        soup = get_soup(codebook_path)
    except TypeError:
        return codebook_dict

    for var in variables:
        pattern = get_pattern(codebook_path, var, sep, default_pattern)
        match = soup.body.find(text=pattern)

        if match:
            m = re.match(pattern, match).groupdict()
            codebook_dict[var] = clean_text(m.get('desc'), sep=m.get('sep'))

    return codebook_dict









