import unittest
from main import *

class PricesTestCase(unittest.TestCase):

    def test_find_a_site(self):
        '''testing function that finds a url of the 'le male' perfumes'''

        url, perfume = find_a_site('jean paul gaultier le male', 'le male')
        self.assertEqual(url, 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-toaletowa-dla-mezczyzn')
        self.assertEqual(perfume, 'le male')

    def test_find_types(self):
        '''testing function that finds the url of a specific type'''

        url, type = choose_type('https://perfumehub.pl/jean-paul-gaultier'
            '-le-male-woda-toaletowa-dla-mezczyzn','woda perfumowana')
        self.assertEqual(url, 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-perfumowana-dla-mezczyzn')
        self.assertEqual(type, 'woda perfumowana')

    def test_find_capacity(self):
        '''testing function that finds the url of a specific capacity'''

        url, cap = choose_capacity('https://perfumehub.pl/jean-paul-gaultier'
            '-le-male-woda-perfumowana-dla-mezczyzn','75  ml')
        self.assertEqual(url, 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-perfumowana-dla-mezczyzn-75-ml')
        self.assertEqual(cap, '75  ml')

    def test_make_dict(self):
        '''testing function that makes a dictionary'''
        dict = make_a_dict(['a','b'],[1, 2])
        self.assertEqual(dict, {'a': 1, 'b': 2})

    
if __name__ =='__main__':
    unittest.main()
