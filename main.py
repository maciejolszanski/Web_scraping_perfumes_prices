import requests
from bs4 import BeautifulSoup

def find_a_site(perfumes_name):
    '''searching for the wanted perfumes and asking user to choose the correct one'''

    # reaplce spaces with + to create correct url
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
        perfume_dict['link'] = 'perfumehub.pl' + link
        perfumes_to_choose_from.append(perfume_dict)

    # If there is more than one perfume found 
    # user have to choose the correct one
    if len(perfumes_to_choose_from) > 1:
    
        print("I have found more than one perfume:")
        num = 1
        for perfume in perfumes_to_choose_from:
            print(f"{str(num)}.\t{perfume['name']}")
            num += 1
        
        user_choice = int(
            input("Type the number of the one you want to check prices: "))
    # if there is only one perfume found it is immediately regarded as correct
    else:
        user_choice = 1
    
    # this is the url of the perfume comparison prices site
    url_correct_perfumes = perfumes_to_choose_from[user_choice-1]['link']
    
    return(url_correct_perfumes)
    
        
if __name__ == '__main__':
    
    perfumes_name = input("What perfumes prices would you like to know? ")

    perfumes_site = find_a_site(perfumes_name)