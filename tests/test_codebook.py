import pytest, os
from codebook import get_soup, get_pattern, extract_codebook, clean_text, create_yaml
from pprint import pprint

dataset_path  = '/Users/programming/PycharmProjects/crime/datasets/ex1/d3.tsv'
codebook_path = '/Users/programming/PycharmProjects/crime/datasets/ex1/Codebooks/d3.pdf'
variables = [
    'AGENCY',
    'YEAR',
    'City',
    'State',
    'Assault-Knife-JAN',
    'ASSAULT-Knife-FEB',
    'ASSAULT-Knife-MAR',
    'MURDER-Knife-JAN',
    'MURDER-Knife-FEB',
    'MURDER-Knife-MAR',
    'Assault-Gun-JAN',
    'ASSAULT-Gun-FEB',
    'ASSAULT-Gun-MAR',
    'MURDER-Gun-JAN',
    'MURDER-Gun-FEB',
    'MURDER-Gun-MAR',
    'V1',
    'V2',
    'V3'
]


def test_get_soup():
    result = get_soup(codebook_path=codebook_path)
    pprint(result.prettify())


def test_get_pattern():
    result = get_pattern(codebook_path=codebook_path, variable=variables[0])
    print(result)


def test_extract_codebook():
    result = extract_codebook(codebook_path=codebook_path, variables=variables)
    print()
    pprint(result)


def test_clean_text():
    text_map = {
        ':\tRecord\tyear\t'             : 'Record year',
        ':\tCity\t\t'                   : 'City',
        ':\tRecord\tstate\t'            : 'Record state',
        ':\tAssaults\tin\tJanuary\t\t'  : 'Assaults in January',
        ':\tAssaults\tin\tFebruary\t'   : 'Assaults in February',
        ':\tAssaults\tin\tMarch\t\t'    : 'Assaults in March',
        ':\tMurders\tin\tJanuary\t'     : 'Murders in January',
        ':\tMurders\tin\tFebruary\t'    : 'Murders in February',
        ':\tMurders\tin\tMarch\t'       : 'Murders in March',
        ':\tRobberies\tin\tJanuary\t\t' : 'Robberies in January',
        ':\tRobberies\tin\tFebruary\t'  : 'Robberies in February',
        ':\tRobberies\tin\tMarch\t\t\t' : 'Robberies in March',
    }

    for (k, v) in text_map.items():
        assert clean_text(k) == v


def test_create_yaml():
    result = create_yaml(dataset_path)
