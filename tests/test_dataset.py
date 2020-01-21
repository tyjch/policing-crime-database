import pytest, yaml
import pandas as pd
from schema import Dataset, Column
from pprint import pprint
from utility import get_stubnames

dataset_path = '/Users/programming/PycharmProjects/crime/datasets/ex1/d1.tsv'


class TestInit:

    def test_init(self):
        instance = Dataset(dataset_path)
        assert instance.path      == "/Users/programming/PycharmProjects/crime/datasets/ex1/d1.tsv"
        assert instance.directory == "/Users/programming/PycharmProjects/crime/datasets/ex1"
        assert instance.file      == "d1.tsv"
        assert instance.name      == 'd1'
        assert instance.extension == 'tsv'


    def test_init_with_bad_path(self):
        with pytest.raises(ValueError):
            instance = Dataset('/directory/datasets/somefile')


    def test_init_with_missing_file(self):
        with pytest.raises(FileNotFoundError):
            instance = Dataset("/Users/programming/PycharmProjects/crime/datasets/ex1/missing_dataset.tsv")


    def test_init_with_wrong_path_type(self):
        with pytest.raises(AttributeError):
            instance = Dataset(3)
