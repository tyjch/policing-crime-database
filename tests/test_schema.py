import pytest, yaml
import pandas as pd
from schema import Dataset, Column
from pprint import pprint
from utility import get_stubnames


paths = [
    '/Users/programming/PycharmProjects/crime/datasets/ex1/d1.tsv',
    '/Users/programming/PycharmProjects/crime/datasets/ex1/d3.tsv',
]

dataset_path = paths[0]


class TestTable:

    def test_table(self):
        assert False


class TestDataset:

    def test_init(self):
        instance = Dataset(dataset_path)
        print()
        print('path:     ', instance.path)
        print('directory:', instance.directory)
        print('file:     ', instance.file)
        print('name:     ', instance.name)
        print('extension:', instance.extension)

    def test_get_codebook(self):
        instance = Dataset(dataset_path)
        variables = ['Agency', 'Year']
        result = instance.get_codebook(variables)
        print()
        pprint(result)

        for v in variables:
            assert v in result.keys()

    def test_get_delimiter(self):
        instance = Dataset(dataset_path)
        result = instance.get_delimiter()
        assert result in ('\t', ',')

    def test_setitem_invalid_type(self):
        invalid_value = 4
        instance = Dataset(dataset_path)
        with pytest.raises(ValueError):
            instance['Column'] = invalid_value

    def test_read(self):
        instance = Dataset(dataset_path)

        instance['Year'].index  = True
        instance['City'].index  = True
        instance['State'].index = True
        instance['Update'].date = True

        v1 = instance['State']
        v1.values = {
            '50': 'California',
            '49': 'Nevada',
            '48': 'Arizona'
        }

        v2 = instance['Murder-JAN']
        v2.values = {
            'a': 0,
            'd': 3,
            'g': 6
        }

        v2 = instance['Murder-FEB']
        v2.values = {
            'b': 1,
            'e': 4,
            'h': 7
        }

        v2 = instance['Murder-MAR']
        v2.values = {
            'c': 2,
            'f': 5,
            'i': 7
        }

        result = instance.read()

        print(); pprint(result)

    def test_dump(self):
        instance = Dataset(dataset_path)
        instance.dump()

    def test_load(self):
        yaml_path = '/Users/programming/PycharmProjects/crime/datasets/ex1/d1.yaml'

        with open(yaml_path) as file:
            doc = yaml.full_load(file)

        print(doc['State'].description)

    def test_wide_table(self):
        instance = Dataset(dataset_path)

        instance['Year'].index   = True
        instance['City'].index   = True
        instance['State'].index  = True
        instance['Agency'].index = True
        instance['Update'].date  = True

        v1 = instance['State']
        v1.values = {
            '50': 'California',
            '49': 'Nevada',
            '48': 'Arizona'
        }

        v2 = instance['Murder-JAN']
        v2.values = {
            'a': 0,
            'd': 3,
            'g': 6
        }

        v2 = instance['Murder-FEB']
        v2.values = {
            'b': 1,
            'e': 4,
            'h': 7
        }

        v2 = instance['Murder-MAR']
        v2.values = {
            'c': 2,
            'f': 5,
            'i': 7
        }

        df = instance.read()

        suffixes = ['JAN', 'FEB', 'MAR']

        print()
        i = df.index.names; pprint(i)
        j = 'Month'
        sep = '-'
        stubnames = get_stubnames(df.columns, suffixes); pprint(stubnames)
        suffix = rf"({'|'.join(suffixes)})"

        df.reset_index(inplace=True)

        result = pd.wide_to_long(
            df  = df,
            i   = i,
            j   = j,
            sep = sep,
            stubnames = stubnames,
            suffix = '\\w{3}'
        )

        df.set_index(keys=i)

        print(result)


class TestColumn:

    def test_convert(self):
        instance = Column(
            identity = 'Column 1',
            name = "Murder-JAN",
            description = "Murders in January",
        )

        instance.values = {'a': 0, 'd': 3, 'g': 6}

        for row in ('a', 'd', 'g'):
            value = instance.converter(row)
            print(value)


