import requests
import re
import datetime

from bs4 import BeautifulSoup
from os import path, mkdir


def find_a_site(perfumes_name):
    '''searching for the wanted perfumes and choosing the correct one'''

    # replace spaces with '+' to create correct url
    perfumes_name_pluses = ''
    for sign in perfumes_name:
        if sign == ' ':
            sign = '+'
        perfumes_name_pluses += sign

    url_of_searching = f'https://perfumehub.pl/search?q={perfumes_name_pluses}'

    # finding a site that shows searching results
    site_searching_html = get_site_html(url_of_searching)

    perfumes_found = site_searching_html.find_all(class_='list-item d-flex')
    
    # creating a list of available perfumes
    perfumes_to_choose_from = []
    
    for perfume_found in perfumes_found:
        #finding perfume name and link to it's site
        name = perfume_found.strong.text.strip()
        link = perfume_found.strong.parent.parent['href'].strip()

        perfume_dict = make_a_dict(
            ['name','link'], [name, 'https://perfumehub.pl' + link])
        perfumes_to_choose_from.append(perfume_dict)

    return perfumes_to_choose_from
    
def choose_type(perfume_url):
    '''check what are the possible types: edt, edp eg.'''

    # finding a site 
    perfume_site_html = get_site_html(perfume_url)    
     
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

    return types_to_choose_from
        
def choose_capacity(perfume_url, preffered_cap=''):
    '''check which capacity are available and let user choose'''
    
    perfume_site_html = get_site_html(perfume_url)   
    perfume_variants = perfume_site_html.find(class_='variant-tiles')

    perfume_capacities = perfume_variants.find_all(class_='variant-tile-title')
    
    capacities_to_choose_from = []

    for capacity in perfume_capacities:

        link = capacity.parent['href'].strip()
        capacity = capacity.text.strip()

        capacity_dict = make_a_dict(
            ['name','link'], [capacity, 'https://perfumehub.pl' + link])

        capacities_to_choose_from.append(capacity_dict)

    return capacities_to_choose_from

def check_prices(perfume_url):
    '''checking prices of this perfume and where to buy it'''
    
    perfume_site_html = get_site_html(perfume_url)   

    perfume_rows = perfume_site_html.find_all(
        class_='row offer border-top mx-0 align-items-center')

    found_prices = []
    for row in perfume_rows:
        shop_tag = row.find(
            class_='col-6 col-md-3 order-3 order-md-1 px-0 '
            'pl-lg-3 shop-name').a

        shop_name = shop_tag.text.strip()
        link = shop_tag['href'].strip()
        
        price_regex = re.compile("\d+.*\d* z??")
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

def create_an_url(list_of_items, items_name, preffered=''):
    '''creating an url for perfumehub based on a list'''

    # getting the preffered name of the perfumes
    if preffered:
        correct_url, chosen_item = _choose_preffered(
            list_of_items, preffered)
    # user chooses the correct one and receives the url 
    else:
        correct_url, chosen_item = _let_user_choose(list_of_items, items_name)

    return correct_url, chosen_item

def get_site_html(url):
    '''gets the site in html formatting'''

    try:
        site = requests.get(url).text
        site_html = BeautifulSoup(site, 'html.parser')
        return site_html

    except:
        print('Sorry, I cannot find such a site.')
        return None
    

def _let_user_choose(items_to_choose_from, item_name):
    '''leting user choose the one item he wants'''

    if len(items_to_choose_from) > 1:
        user_choice = _ask_user(items_to_choose_from, item_name)
    # if there is only one item found it is immediately regarded as correct
    else:
        print(f"I have found only one {item_name}: "
            f"{items_to_choose_from[0]['name']}")
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
    
    # asking user about the perfume name
    perfume_name = input("What perfumes prices would you like to know? ")

    preffered_values = ['','','']
    types_of_values = ['Perfume:','Type:', 'Capacity:']

    # print instrucions
    print("Type preffered values to automate the process\n"
        "Submit each value with ENTER\n"
        "If you do not know the values and want to go through the process"
        "press 'q' and sumbit with ENTER\n")

    # if user knows exact values of the needed items he/she can type them now 
    # it will make the process last a little shorter 
    # if he/she does not know he can skip it by pressing 'q'
    num = 0
    for value in types_of_values:
        value = input(f"{value} ")
        if value == 'q':
            break
        else:
            preffered_values[num] = value
            num += 1

    # finding perfumes that match a perfume name given by user 
    # and finding its url
    available_perfumes = find_a_site(perfume_name)
    perfumes_site_url, chosen_perfume = create_an_url(available_perfumes,
        'perfume', preffered_values[0])


    available_types = choose_type(perfumes_site_url)
    wanted_type_url, chosen_type = create_an_url(available_types, 'type', 
        preffered_values[1])

    available_capacities = choose_capacity(wanted_type_url)
    wanted_capacity_url, chosen_capacity = create_an_url(available_capacities,
        'capacity', preffered_values[2])

    perfume_prices = check_prices(wanted_capacity_url)
    write_prices_to_txt(
        perfume_prices, chosen_perfume, chosen_type, chosen_capacity)
