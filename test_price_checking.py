import unittest
from main import *

class PricesTestCase(unittest.TestCase):

    def setUp(self):
        '''creating lists of available elements'''

        self.available_perfumes = [{'name': 'fleur du male', 'link': 'https://perfumehub.pl/jean-paul-gaultier-fleur-du-male-woda-toaletowa-dla-mezczyzn'}, {'name': 'le beau male', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-beau-male-woda-toaletowa-dla-mezczyzn'}, {'name': 'le male', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-toaletowa-dla-mezczyzn'}, {'name': 'le male aviator', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-aviator-woda-toaletowa-dla-mezczyzn'}, {'name': 'le male eau fraiche gaultier airlines edition', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-eau-fraiche-gaultier-airlines-edition-woda-toaletowa-dla-mezczyzn'}, {'name': 'le male essence de parfum', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-essence-de-parfum-woda-perfumowana-dla-mezczyzn'}, {'name': 'le male in the navy', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-in-the-navy-woda-toaletowa-dla-mezczyzn'}, {'name': 'le male le parfum', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-le-parfum-woda-perfumowana-dla-mezczyzn'}, {'name': 'le male on board', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-on-board-woda-toaletowa-dla-mezczyzn'}, {'name': 'le male pride', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-pride-woda-toaletowa-dla-mezczyzn'}, {'name': 'le male summer fragrance', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-summer-fragrance-woda-toaletowa-dla-mezczyzn'}, {'name': 'le male terrible', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-terrible-woda-toaletowa-dla-mezczyzn'}, {'name': 'le male x supreme', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-x-supreme-woda-toaletowa-dla-mezczyzn'}, {'name': 'ultra male', 'link': 'https://perfumehub.pl/jean-paul-gaultier-ultra-male-woda-toaletowa-dla-mezczyzn'}]

        self.available_types = [{'name': 'woda perfumowana', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-perfumowana-dla-mezczyzn'}, {'name': 'woda toaletowa', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-toaletowa-dla-mezczyzn'}, {'name': 'woda po goleniu', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-po-goleniu-dla-mezczyzn'}]

        self.available_capacities = [{'name': '200  ml', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-perfumowana-dla-mezczyzn-200-ml'}, {'name': '125  ml tester', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-perfumowana-dla-mezczyzn-125-ml-tester'}, {'name': '75  ml', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-perfumowana-dla-mezczyzn-75-ml'}, {'name': '7  ml  zestaw', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-perfumowana-dla-mezczyzn-7-ml-zestaw'}, {'name': 'wszystkiewarianty', 'link': 'https://perfumehub.pl/jean-paul-gaultier-le-male-woda-perfumowana-dla-mezczyzn?all=true'}]

    def test_find_a_site(self):
        '''testing function that finds a url of the 'le male' perfumes'''

        available = find_a_site('jean paul gaultier le male')
        self.assertEqual(available, self.available_perfumes)

    def test_find_types(self):
        '''testing function that finds the url of a specific type'''

        available = choose_type('https://perfumehub.pl/jean-paul-gaultier-le'
            '-male-woda-toaletowa-dla-mezczyzn')
        self.assertEqual(available, self.available_types)

    def test_find_capacities(self):
        '''testing function that finds the available capacities'''

        available = choose_capacity('https://perfumehub.pl/'
            'jean-paul-gaultier-le-male-woda-perfumowana-dla-mezczyzn')
        self.assertEqual(available, self.available_capacities)

    def test_find_url(self):
        '''testing function that finds the url'''

        url, chosen_item = create_an_url(self.available_perfumes, 'item',
            'le male')
        self.assertEqual(url, 'https://perfumehub.pl/'
        'jean-paul-gaultier-le-male-woda-toaletowa-dla-mezczyzn')
        self.assertEqual(chosen_item, 'le male')

    def test_make_dict(self):
        '''testing function that makes a dictionary'''
        dict = make_a_dict(['a','b'],[1, 2])
        self.assertEqual(dict, {'a': 1, 'b': 2})

    
if __name__ =='__main__':
    unittest.main()
