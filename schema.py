import yaml
import pandas as pd
from yaml import YAMLObject
from pprint import pprint
from codebook import extract_codebook

pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'left')

delimiters = {
    'tsv': '\t',
    'csv': ','
}



class Table(YAMLObject):
    yaml_tag = u'!Table'

    def __init__(self, name):
        self.name = name

    def to_sql(self):
        pass



class Dataset(YAMLObject):
    yaml_tag = u'!Dataset'



    def __init__(self, path):
        self.path = path
        self.directory, self.file = path.rsplit(sep='/', maxsplit=1)
        self.name, self.extension = self.file.rsplit(sep='.', maxsplit=1)
        self.yaml = f"{self.directory}/{self.name}.yaml"
        self.columns = {}


    @property
    def df(self):
        names = [c.name for c in self.columns.values()]
        index_col = [c.name for c in self.columns.values() if c.index]
        use_cols = [c.name for c in self.columns.values() if c.include]
        converters = {c.name: c.converter for c in self.columns.values()}
        parse_dates = [c.name for c in self.columns.values() if c.date]
        dtype = {c.name: c.dtype for c in self.columns.values() if c.dtype}

        df = pd.read_csv(
            filepath_or_buffer=self.path,
            delimiter=delimiters[self.extension],
            header=0,
            encoding='latin1',
            names=names,
            index_col=index_col,
            usecols=use_cols,
            dtype=dtype,
            parse_dates=parse_dates,
            converters=converters
        )

        return df


    def __setitem__(self, key, value):
        if isinstance(value, Column):
            self.columns[key] = value
        else:
            raise ValueError("Only objects of type `Column` are allowed as values")


    def __getitem__(self, key):
        return self.columns[key]


    def __iter__(self):
        return iter(self.columns)


    def __repr__(self):
        return f"{self.name} {self.columns}"


    def get_columns(self):
        df = pd.read_csv(
            filepath_or_buffer=self.path,
            delimiter=delimiters[self.extension],
            encoding='latin1',
            nrows=0
        )

        codebook = extract_codebook(
            codebook_path = f"{self.directory}/Codebooks/{self.name}.pdf",
            variables = df.columns,
            sep = '',
            default_pattern = "^(\\n)*(?P<desc>.+)(?P<sep>{sep})(?P<var>{var})"
        )

        pprint(codebook)

        for name, description in codebook.items():
            self[name] = Column(
                identity    = name,
                name        = name,
                description = description,
            )


    def restore(self):
        # TODO: Restore `self` from yaml file
        pass


    def dump(self):
        with open(self.yaml, 'w') as file:
            docs = yaml.dump(self, file)



class Column(YAMLObject):
    yaml_tag = u'!Column'

    def __init__(self, identity, name, description='', dtype=None, index=False, include=True, date=False):
        """
        Parameters
        ----------
        identity : str
            The name of the column in the header of the source dataset file.
        name : str
            The name we want to use as the column name in the dataset/table.
        description : str
            Extracted from the corresponding codebook if available. Could possibly be used to rename the variable.
        dtype : str, optional
            A label of the type to try and interpret the values of the column as.
        index : bool, optional
            If True, this indicates the column should be used as (part of) the index of the dataframe.
        include : bool, optional
            If False, this indicates the column should not be loaded in the dataframe.
        date : bool, optional
            If True, this indicates that the column values should be parsed as date/datetimes.
        """

        self.id          = identity
        self.name        = name
        self.dtype       = dtype
        self.description = description
        self.index       = index
        self.include     = include
        self.date        = date
        self.values      = {}


    def __repr__(self):
        return f"Column: {self.id}"


    def __setitem__(self, key, value):
        """
        Parameters
        ----------
        key : int or str (usually)
            Represents an existing value in the column that we want to replace with a new value.
            Must be able to be coerced to a str.
        value :
            Represents the value we want to replace the key with.
        """
        self.values[str(key)] = value


    def __getitem__(self, key):
        return self.values[str(key)]


    def converter(self, row):
        row = str(row)
        return self.values.get(row, row)




