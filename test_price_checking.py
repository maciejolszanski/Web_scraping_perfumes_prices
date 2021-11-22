from io import DEFAULT_BUFFER_SIZE
import unittest
from main import *

class PricesTestCase(unittest.TestCase):

    def test_find_a_site(self):
        '''testing function that finds a url of the 'le male' perfumes'''

        url, perfume = find_a_site('jean paul gaultier le male', 'le male')
        self.assertEqual(url, 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-toaletowa-dla-mezczyzn')
        self.assertEqual(perfume, 'le male')

    #def test_find_types(self):
    
    
if __name__ =='__main__':
    unittest.main()
