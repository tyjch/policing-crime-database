import io, re
import pandas as pd
from bs4 import BeautifulSoup
from pdfminer.converter import HTMLConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def clean_text(text: str):
    text = ' '.join(text.split())
    text = text.replace(':', '')
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


def get_pattern(codebook_path: str, variable: str):
    codebook = codebook_path.rsplit(sep='/', maxsplit=1)[-1]

    default_pattern = f"^(\\t)*({variable}):(.+)"
    patterns = {
        'd1.pdf': f"^(\\t)*({variable}):(.+)",
        'd2.pdf': f"^(\\t)*({variable}):(.+)"
    }

    pattern = patterns.get(codebook, default_pattern)
    return re.compile(pattern, flags=re.I)


def extract_codebook(codebook_path, variables):
    codebook_dict = {}

    try:
        soup = get_soup(codebook_path)
    except TypeError:
        return codebook_dict

    for var in variables:
        pattern = get_pattern(codebook_path, var)
        match = soup.body.find(text=pattern)

        if match:
            parts = match.split(var.upper())
            codebook_dict[var] = clean_text(parts[-1])

    return codebook_dict


def create_yaml(dataset_path):
    filename = dataset_path.rsplit(sep='/', maxsplit=1)[-1]; print(filename)
    name = filename.split(sep='.')[0]; print(name)


    df = pd.read_csv(
        filepath_or_buffer=dataset_path,
        delimiter='\t',
        encoding='latin1',
        nrows=1
    )






