import requests
import info
from bs4 import BeautifulSoup


def get_page_soup(url):
    '''Берет url страницы и возвращает объект soup
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def get_all_of_ids(soup):
    '''вытаскивает все СНИЛСы из таблицы и возвращает массив с ними'''
    ids = soup.findAll('td', class_= 'fio')
    filtered_ids = [data.text for data in ids]
    return filtered_ids

def get_my_place(ids, snils):
    ''' Принимает массив СНИЛСов и находит в нем место указанного номера СНИЛС.
    Если такого номера нет, то возвращает -1
    '''
    for i, ID in enumerate(ids):
        if ID == snils:
            return i
    return -1

def get_direction_name(soup):
    '''Принимает объект soup и возвращает название направления'''
    name = soup.findAll('h1')[0].text.split('\n')[1]
    print('ALERT')
    return name

def my_place(url,snils):
    '''Берет адрес страницы и искомый СНИЛС и возвращает его место в рейтинге
    '''
    soup = get_page_soup(url)
    ids = get_all_of_ids(soup)
    place = get_my_place(ids, snils)
#   name = get_direction_name(soup)
    return place, count_accepts_before_me(place, soup)

def count_accepts_before_me(place, soup):
    accents = soup.findAll('td', class_ = 'accepted')
    filtered_accents = [data.text for data in accents]
    count = filtered_accents[:place].count('да')
    return count

def get_all_of_my_places(urls = info.urls, snils = info.my_snils_for_MIREA, directions = info.directions_of_MIREA):
    '''Берет все указанные url и находит в каждом из них место указанного номера СНИЛС
    Возвращает строку с указанием направления и номера занятого места'''
    return_my_places = ''
    numdir = 0
    for url in urls:
        place = my_place(url,snils)
        return_my_places+= str(directions[numdir]) +  '\n    Место:' + str(place[0]) + '\n    Согласий выше: '+ str(place[1]) + '\n'
        numdir+=1
    return return_my_places
print(get_all_of_my_places())