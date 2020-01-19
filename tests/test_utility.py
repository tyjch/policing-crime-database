import pytest
from utility import get_stubnames
from pprint import pprint

def test_get_stubnames():
    strings = [
        'Assault-Knife-JAN',
        'Assault-Knife-FEB',
        'Assault-Gun-JAN',
        'Assault-Gun-FEB',
        'Murder-Knife-JAN',
        'Murder-Knife-FEB',
        'Murder-Gun-JAN',
        'Murder-Gun-FEB'
    ]

    stubnames = get_stubnames(strings, suffixes=['JAN', 'FEB'])
    print(); pprint(stubnames)
    assert stubnames == {'Murder-Gun', 'Murder-Knife', 'Assault-Knife', 'Assault-Gun'}



