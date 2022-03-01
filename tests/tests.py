#######################################################################
# Testing the functionality of the functions in starwars_api module
# Author : Saikrishna Javvadi
# Date : 13/12/2021
# Version : 1.0
# Description : This is a test file for the starwars_api module
# References : https://realpython.com/python-testing/
#              https://docs.python.org/3/library/unittest.html
#######################################################################


import unittest
from .. import starwars_api


class TestClass(unittest.TestCase):

    def test_get_names_list(self):
        res = starwars_api.get_names_list('https://swapi.dev/api/people')
        res = list(res)
        self.assertEqual(len(res), 82, f'resulting list is {len(res)} rather than 82')

    def test_get_people_data(self):
        res = starwars_api.get_people_data('https://swapi.dev/api/people/')
        res = list(res)
        self.assertEqual(len(res), 82, f'resulting list is {len(res)} rather than 82')

    def test_include_keys(self):
        res = starwars_api.include_keys({'name': 'Saikrishna', 'height': 176, 'weight': 83, 'age': 24},
                                        ['name', 'height'])
        self.assertEqual(res, {'name': 'Saikrishna', 'height': 176}, f'resulting dict is incorrect')

    def test_find(self):
        res = starwars_api.find('name', 'Luke Skywalker')
        self.assertEqual(res, [{'hair_color': 'blond', 'height': '172', 'mass': '77', 'name': 'Luke Skywalker'}],
                         f'resulting dict is incorrect')
        self.assertEqual(res[0]['height'], '172', f'resulting list is {len(res)} rather than 1')


if __name__ == '__main__':
    unittest.main()
