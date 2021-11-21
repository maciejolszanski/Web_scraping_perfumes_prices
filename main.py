import requests
from bs4 import BeautifulSoup

def find_a_site(perfumes_name):
    '''searching for the wanted perfumes and asking user to choose the correct one'''

    # replace spaces with '+' to create correct url
    perfumes_name_pluses = ''
    for sign in perfumes_name:
        if sign == ' ':
            sign = '+'
        perfumes_name_pluses += sign

    url_of_searching = f'https://perfumehub.pl/search?q={perfumes_name_pluses}'

    # finding a site that shows searching results
    site_searching = requests.get(url_of_searching).text
    site_searching_html = BeautifulSoup(site_searching, 'html.parser')
    perfumes_found = site_searching_html.find_all(class_='list-item d-flex')
    
    perfumes_to_choose_from = []
    
    # giving user a response of found perfume kinds
    for perfume_found in perfumes_found:
        #finding perfume name and link to it's site
        name = perfume_found.strong.text
        link = perfume_found.strong.parent.parent['href']

        perfume_dict = {}
        perfume_dict['name'] = name
        perfume_dict['link'] = 'http://perfumehub.pl' + link
        perfumes_to_choose_from.append(perfume_dict)

    # user choosesthe correct perfumes, function returns the url
    correct_url = let_user_choose(perfumes_to_choose_from, 'perfume')
    
    return(correct_url)
    
def choose_type(perfume_url):
    '''check what are the possible types: edt, edp eg.'''

    perfume_site = requests.get(perfume_url).text
    perfume_site_html = BeautifulSoup(perfume_site, 'html.parser')
    perfume_type = perfume_site_html.find(class_='mt-4')
    perfume_tag = perfume_type.find_all(name='a')

    # create list of available types of perfume and store it in a list o dicts
    types_to_choose_from = []
    for tag in perfume_tag:
        type_dict = {}
        
        type = tag.text
        link = tag['href']
        type_dict['name'] = type
        type_dict['link'] = 'http://perfumehub.pl' + link

        types_to_choose_from.append(type_dict)

    # user chooses the correct one and receives the url 
    correct_url = let_user_choose(types_to_choose_from, 'type')

    return correct_url
        
def choose_capacity(perfume_url):
    '''check which capacity are available and let user choose'''
    perfume_site = requests.get(perfume_url).text
    perfume_site_html = BeautifulSoup(perfume_site, 'html.parser')
    perfume_variants = perfume_site_html.find(class_='variant-tiles')

    perfume_capacities = perfume_variants.find_all(class_='variant-tile-title')
    
    capacities_to_choose_from = []

    for capacity in perfume_capacities:
        capacity_dict = {}

        link = capacity.parent['href']
        capacity = capacity.text
        capacity_dict['name'] = capacity
        capacity_dict['link'] = link

        capacities_to_choose_from.append(capacity_dict)

    correct_url = let_user_choose(capacities_to_choose_from, 'capacity')

    return(correct_url)


def let_user_choose(items_to_choose_from, item_name):
    '''leting user choose the one item he wants'''

    if len(items_to_choose_from) > 1:
        print(f"I have found more than one {item_name}:")
        num = 1
        for item in items_to_choose_from:
            print(f"{str(num)}.\t{item['name']}")
            num += 1
        
        user_choice = int(
            input("Type the number of the one you want to check prices for: "))
    # if there is only one item found it is immediately regarded as correct
    else:
        print(f'I have found only one {item_name}: {items_to_choose_from[0]}')
        user_choice = 1

    url_correct_perfumes = items_to_choose_from[user_choice-1]['link']

    return url_correct_perfumes

if __name__ == '__main__':
    
    perfume_name = input("What perfumes prices would you like to know? ")

    perfumes_site_url = find_a_site(perfume_name)
    wanted_type_url = choose_type(perfumes_site_url)
    wanted_capacity_url = choose_capacity(wanted_type_url)
    print(wanted_capacity_url)
