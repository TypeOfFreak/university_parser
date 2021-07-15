import requests
import info
from bs4 import BeautifulSoup

def page_download(url):
    '''Берет url страницы и возвращает объект soup
    '''
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def get_all_id(soup):
    '''вытаскивает все СНИЛСы из таблицы и возвращает массив с ними'''
    ids = soup.findAll('td', class_= 'fio')
    filtered_ids = [data.text for data in ids]
    return filtered_ids

def get_place(ids,snils):
    ''' Принимает массив СНИЛСов и находит в нем место указанного номера СНИЛС.
    Если такого номера нет, то возвращает -1
    '''
    for i, ID in enumerate(ids):
        if ID == snils:
            return i
    return -1
def get_name(soup):
    '''Принимает объект soup и возвращает название направления'''
    name = soup.findAll('h1')[0].text.split('\n')[1]
    return name
def my_place(url,snils):
    '''Берет адрес страницы и искомы СНИЛС и возвращает его место в рейтинге
    '''
    soup = page_download(url)
    ids = get_all_id(soup)
    place = get_place(ids,snils)
    name = get_name(soup)
    return name[2:], place, count_accepts(place,soup)

def count_accepts(place, soup):
    accents = soup.findAll('td', class_ = 'accepted')
    filtered_accents = [data.text for data in accents]
    count = filtered_accents[:place].count('да')
    return count

def get_my_places(urls = info.urls, snils = info.snils):
    '''Берет все указанные url и находит в каждом из них место указанного номера СНИЛС
    Возвращает строку с указанием направления и номера занятого места'''
    places = ''
    for url in urls:
        place = my_place(url,snils)
        places+= str(place[0]) +  '\n    Место:' + str(place[1]) + '\n    Согласий выше: '+ str(place[2]) + '\n'
    return places