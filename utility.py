import re
from collections import defaultdict
from pprint import pprint


def get_stubnames(strings: list, suffixes:list, sep='-'):
    suffixes = '|'.join(suffixes)
    pattern = re.compile(rf"(?P<stub>.*){sep}(?P<suffix>{suffixes})")

    stubs = set()
    for s in strings:
        m = re.match(pattern, s)
        if m:
            m = m.groupdict()
            stubs.add(m.get('stub'))

    return stubs








