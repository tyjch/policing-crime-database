import pytest, os, bs4
from codebook import get_soup, get_pattern, extract_codebook, clean_text
from pprint import pprint

dataset_path  = '/Users/programming/PycharmProjects/crime/datasets/ex1/d3.tsv'
codebook_path = '/Users/programming/PycharmProjects/crime/datasets/OK/Codebooks/2013.pdf'



class TestGetSoup:


    def test_get_soup(self):
        result = get_soup(codebook_path)
        print(result)
        assert isinstance(result, bs4.BeautifulSoup)


    def test_with_question_sep(self):
        result = get_soup('/Users/programming/PycharmProjects/crime/datasets/ex1/Codebooks/question_sep.pdf')
        print(result.prettify())
        assert isinstance(result, bs4.BeautifulSoup)


    def test_with_mixed_sep(self):
        result = get_soup('/Users/programming/PycharmProjects/crime/datasets/ex1/Codebooks/mixed_sep.pdf')
        print(result.prettify())
        assert isinstance(result, bs4.BeautifulSoup)


    def test_with_alternate_pattern(self):
        result = get_soup('/Users/programming/PycharmProjects/crime/datasets/ex1/Codebooks/alternate_pattern.pdf')
        print(result.prettify())
        assert isinstance(result, bs4.BeautifulSoup)


    def test_get_soup_with_bad_path(self):
        with pytest.raises(FileNotFoundError):
            result = get_soup('/Users/programming/PycharmProjects/crime/datasets/ex1/Codebooks/d0.pdf')


    # FIXME: Takes forever to run
    '''
    def test_get_soup_with_bad_type(self):
        with pytest.raises(FileNotFoundError):
            result = get_soup(3)
    '''



class TestCleanText:

    def test_clean_text(self):
        text_map = {
            ':\tRecord\tyear\t': 'Record year',
            ':\tCity\t\t': 'City',
            ':\tRecord\tstate\t': 'Record state',
            ':\tAssaults\tin\tJanuary\t\t': 'Assaults in January',
            ':\tAssaults\tin\tFebruary\t': 'Assaults in February',
            ':\tAssaults\tin\tMarch\t\t': 'Assaults in March',
            ':\tMurders\tin\tJanuary\t': 'Murders in January',
            ':\tMurders\tin\tFebruary\t': 'Murders in February',
            ':\tMurders\tin\tMarch\t': 'Murders in March',
            ':\tRobberies\tin\tJanuary\t\t': 'Robberies in January',
            ':\tRobberies\tin\tFebruary\t': 'Robberies in February',
            ':\tRobberies\tin\tMarch\t\t\t': 'Robberies in March',
        }

        for (k, v) in text_map.items():
            assert clean_text(k) == v


    def test_clean_text_with_single_word(self):
        result = clean_text('ASSAULT')
        assert result == 'ASSAULT'


    def test_clean_text_with_int(self):
        result = clean_text(3)
        assert result == '3'


    def test_with_multiple_separators(self):
        text_map = {
            '? Agency': 'Agency',
            ': Agency': 'Agency',
            '- Agency': 'Agency',
        }

        for (k, v) in text_map.items():
            assert clean_text(k, sep=['?', ':', '-']) == v



class TestGetPattern:

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
        'Update'
    ]

    def test_get_pattern(self):
        result = get_pattern(
            codebook_path=codebook_path,
            variable=self.variables[0]
        )
        print(result)


    def test_with_question_sep(self):
        result = get_pattern(
            codebook_path = '/Users/programming/PycharmProjects/crime/datasets/ex1/Codebooks/question_sep.pdf',
            variable = self.variables[0],
            sep = r'\?'
        )
        print(result)


    def test_with_mixed_sep(self):
        result = get_pattern(
            codebook_path = '/Users/programming/PycharmProjects/crime/datasets/ex1/Codebooks/mixed_sep.pdf',
            variable = self.variables[0],
            sep = [':', '-', r'\?']
        )
        print(result)


    def test_with_alternate_pattern(self):
        result = get_pattern(
            codebook_path = '/Users/programming/PycharmProjects/crime/datasets/ex1/Codebooks/alternate_pattern.pdf',
            variable = self.variables[0],
            sep = [':', '-', r'\?'],
            default_pattern = "^(\\t)(abc|xyz)({var})({sep})(.+)"
        )
        print(result)



class TestExtractCodebook:

    variables = {
        'AGENCY': 'Name of Agency',
        'YEAR': 'Record year',
        'City': 'City',
        'State': 'Record state',
        'Assault-JAN': 'Assaults in January',
        'ASSAULT-FEB': 'Assaults in February',
        'ASSAULT-MAR': 'Assaults in March',
        'MURDER-JAN': 'Murders in January',
        'MURDER-FEB': 'Murders in February',
        'MURDER-MAR': 'Murders in March',
        'V1': 'Rapes in January',
        'V2': 'Rapes in February',
        'V3': 'Rapes in March',
        'Update': 'Last Update'
    }

    def test_extract_codebook(self):
        '''
        variables = {
            'AGENCY': 'Name of Agency',
            'YEAR': 'Record year',
            'City': 'City',
            'State': 'Record state',
            'Assault-Knife-JAN': 'Assaults with knife in January',
            'ASSAULT-Knife-FEB': 'Assaults with knife in February',
            'ASSAULT-Knife-MAR': 'Assaults with knife in March',
            'MURDER-Knife-JAN': 'Murders with knife in January',
            'MURDER-Knife-FEB': 'Murders with knife in February',
            'MURDER-Knife-MAR': 'Murders with knife in March',
            'Assault-Gun-JAN': 'Assaults with gun in January',
            'ASSAULT-Gun-FEB': 'Assaults with gun in February',
            'ASSAULT-Gun-MAR': 'Assaults with gun in March',
            'MURDER-Gun-JAN': 'Murders with gun in January',
            'MURDER-Gun-FEB': 'Murders with gun in February',
            'MURDER-Gun-MAR': 'Murders with gun in March',
            'Update': 'Last Update'
        }
        '''

        variables = {
            'V1': 'Empty',
            'V2': 'Empty',
            'V3': 'Empty',
        }
        result = extract_codebook(
            codebook_path=codebook_path,
            variables=variables,
        )

        print(); pprint(result)

        '''
        for v in variables:
            assert result[v] == variables[v]
        '''

    def test_with_question_sep(self):
        result = extract_codebook(
            codebook_path = '/Users/programming/PycharmProjects/crime/datasets/ex1/Codebooks/question_sep.pdf',
            variables=self.variables,
            sep=r'\?'
        )

        print(); pprint(result)

        for v in self.variables:
            assert result[v] == self.variables[v]


    def test_with_mixed_sep(self):
        result = extract_codebook(
            codebook_path = '/Users/programming/PycharmProjects/crime/datasets/ex1/Codebooks/mixed_sep.pdf',
            variables=self.variables,
            sep=[':', '-', r'\?']
        )
        print(); pprint(result)

        for v in self.variables:
            assert result[v] == self.variables[v]


    def test_with_alternate_pattern(self):
        result = extract_codebook(
            codebook_path = '/Users/programming/PycharmProjects/crime/datasets/ex1/Codebooks/alternate_pattern.pdf',
            variables=self.variables,
            sep=[':', '-', r'\?'],
            #default_pattern=r"^(\t)(abc|xyz)({var})({sep})(.+)"
            default_pattern=r"^.*(abc|xyz)(?P<var>{var})(?P<sep>{sep})(?P<desc>.+)"
        )
        print(); pprint(result)

        for v in self.variables:
            assert result[v] == self.variables[v]
