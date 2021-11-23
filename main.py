import requests
import re
import datetime

from bs4 import BeautifulSoup
from os import path, mkdir


def find_a_site(perfumes_name, preffered_name=''):
    '''searching for the wanted perfumes and choosing the correct one'''

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
        name = perfume_found.strong.text.strip()
        link = perfume_found.strong.parent.parent['href'].strip()

        perfume_dict = make_a_dict(
            ['name','link'], [name, 'https://perfumehub.pl' + link])
        perfumes_to_choose_from.append(perfume_dict)

    # getting the preffered name of the perfumes
    if preffered_name:
        correct_url, chosen_perfume = _choose_preffered(
            perfumes_to_choose_from, preffered_name)
    else:
        # user chooses the correct perfumes, function returns the url
        correct_url, chosen_perfume = _let_user_choose(
            perfumes_to_choose_from, 'perfume')
        
    return correct_url, chosen_perfume
    
def choose_type(perfume_url, preffered_type=''):
    '''check what are the possible types: edt, edp eg.'''

    perfume_site = requests.get(perfume_url).text
    perfume_site_html = BeautifulSoup(perfume_site, 'html.parser')
    perfume_type = perfume_site_html.find(class_='mt-4')
    perfume_tag = perfume_type.find_all(name='a')

    # create list of available types of perfume and store it in a list o dicts
    types_to_choose_from = []
    for tag in perfume_tag:

        pefume_type = tag.text.strip()
        link = tag['href'].strip()

        type_dict = make_a_dict(
            ['name','link'], [pefume_type, 'https://perfumehub.pl' + link])
        types_to_choose_from.append(type_dict)
    # getting the preffered name of the perfumes
    if preffered_type:
        correct_url, chosen_type = _choose_preffered(
            types_to_choose_from, preffered_type)
    # user chooses the correct one and receives the url 
    else:
        correct_url, chosen_type = _let_user_choose(types_to_choose_from, 'type')

    return correct_url, chosen_type
        
def choose_capacity(perfume_url, preffered_cap=''):
    '''check which capacity are available and let user choose'''
    perfume_site = requests.get(perfume_url).text
    perfume_site_html = BeautifulSoup(perfume_site, 'html.parser')
    perfume_variants = perfume_site_html.find(class_='variant-tiles')

    perfume_capacities = perfume_variants.find_all(class_='variant-tile-title')
    
    capacities_to_choose_from = []

    for capacity in perfume_capacities:

        link = capacity.parent['href'].strip()
        capacity = capacity.text.strip()

        capacity_dict = make_a_dict(
            ['name','link'], [capacity, 'https://perfumehub.pl' + link])

        capacities_to_choose_from.append(capacity_dict)

    if preffered_cap:
        correct_url, chosen_capacity = _choose_preffered(
            capacities_to_choose_from, preffered_cap)
    else:
        correct_url, chosen_capacity = _let_user_choose(
            capacities_to_choose_from,'capacity')

    return correct_url, chosen_capacity

def check_prices(perfume_url):
    '''checking prices of this perfume and where to buy it'''
    perfume_site = requests.get(perfume_url).text
    perfume_site_html = BeautifulSoup(perfume_site, 'html.parser')

    perfume_rows = perfume_site_html.find_all(
        class_='row offer border-top mx-0 align-items-center')

    found_prices = []
    for row in perfume_rows:
        shop_tag = row.find(
            class_='col-6 col-md-3 order-3 order-md-1 px-0 '
            'pl-lg-3 shop-name').a

        shop_name = shop_tag.text.strip()
        link = shop_tag['href'].strip()
        
        price_regex = re.compile("\d+.*\d* zł")
        price = row.find(text=price_regex).strip()

        price_dict = make_a_dict(
            ['shop','price','link'], 
            [shop_name, price, 'https://perfumehub.pl' + link])
    
        found_prices.append(price_dict)

    return found_prices

def make_a_dict(dict_keys, dict_values):
    '''making a dictionary from given keys and values'''
    dict = {}
    num = 0
    for key in dict_keys:
        dict[key] = dict_values[num]
        num += 1
    
    return dict
    
def _let_user_choose(items_to_choose_from, item_name):
    '''leting user choose the one item he wants'''

    if len(items_to_choose_from) > 1:
        user_choice = _ask_user(items_to_choose_from, item_name)
    # if there is only one item found it is immediately regarded as correct
    else:
        print(f"I have found only one {item_name}: "
            "{items_to_choose_from[0]['name']}")
        user_choice = 1

    url_correct_perfumes = items_to_choose_from[user_choice-1]['link']
    chosen_item = items_to_choose_from[user_choice-1]['name']

    return url_correct_perfumes, chosen_item

def _ask_user(items, item_name):
    '''asking user to make a choice'''

    print(f"I have found more than one {item_name}:")
    num = 1
    for item in items:
        print(f"{str(num)}.\t{item['name']}")
        num += 1
        
    user_choice = int(input(
        "Type the number of the one you want to check prices for: "))

    return user_choice

def _choose_preffered(items_to_choose_from, preffered_item):
    '''chosing item without asking user'''

    chosen_item_name, chosen_item_link = ['','']

    for item in items_to_choose_from:

        if item['name'] == preffered_item:
            chosen_item_name = item['name']
            chosen_item_link = item['link']

    return chosen_item_link, chosen_item_name

def write_prices_to_txt(prices, perfume_name, perfume_type, capacity): 
    '''Writing found perfume prices to .txt file'''

    localtime_struct = datetime.datetime.now()
    local_date = localtime_struct.strftime('%x')
    local_time = localtime_struct.strftime('%X')

    cor_date = _format_string_to_txt(local_date)
    cor_time = _format_string_to_txt(local_time)
    cor_name = _format_string_to_txt(perfume_name)
    cor_type = _format_string_to_txt(perfume_type)
    cor_cap = _format_string_to_txt(capacity)

    directory_name = 'results'
    filename = (f'{cor_name}_{cor_type}_{cor_cap}_'
        f'{cor_date}_{cor_time}.txt')

    file_path = directory_name + '/' + filename

    #checking if such directory exists and creating it if it does not
    if not path.exists(directory_name):
        mkdir(directory_name)
    # writing results to file
    with open(file_path, 'w') as f:
        f.write(f"{perfume_name.title()}\t\t{perfume_type}\t\t{capacity}"
            f"\t\t{local_date} {local_time}\n\n")
        for element in prices:
            line = f"{element['price']}\t{element['shop']}\t\t{element['link']}\n"
            f.write(line)

def _format_string_to_txt(string):
    '''
    removing disallowed signs form string, repalcing them with _
    i could also use string.replace('/','_') eg., 
    but i decided to this function to replace all disallowed signs
    '''
    corrected_string = ''

    for char in string:
        if char == '/' or char == ':' or char == ' ' or char =='.' or char ==',':
            char = '_'
        corrected_string += char

    return corrected_string


if __name__ == '__main__':
    
    perfume_name = input("What perfumes prices would you like to know? ")

    perfumes_site_url, chosen_perfume = find_a_site(perfume_name, 'le male')
    wanted_type_url, chosen_type = choose_type(perfumes_site_url, 'woda perfumowana')
    wanted_capacity_url, chosen_capacity = choose_capacity(wanted_type_url, '75  ml')

    perfume_prices = check_prices(wanted_capacity_url)
    write_prices_to_txt(
        perfume_prices, chosen_perfume, chosen_type, chosen_capacity)