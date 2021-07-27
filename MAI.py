from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import info
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

def make_driver():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path= '/media/lucas/Staff/Projects/university_parser/chromedriver/chromedriver', options=options)
    driver.get('https://priem.mai.ru/rating/')
    return driver

def choose_the_option(driver, id, num_of_down_clicks):
    select = driver.find_element_by_id(id)
    select.click()

    actions = ActionChains(driver)
    for _ in range(num_of_down_clicks):
        time.sleep(.1)
        actions.send_keys(Keys.DOWN)
    actions.send_keys(Keys.ENTER)
    actions.perform()

def choose_options(driver):
    ids = ['place', 'level_select', 'pay_select', 'form_select']
    num_of_down_clicks = [1, 2, 1, 1]
    for i in range(4):
        time.sleep(.2)
        choose_the_option(driver, ids[i], num_of_down_clicks[i])

def get_table(soup):
    return soup.findAll('table', class_='table')[-1]

def get_my_place_by_snils_list(snils_list, my_snils):
    for i in range(len(snils_list)):
        if snils_list[i].text==my_snils:
            return i+1
    return -1

def get_my_place_and_accepts_before_me(driver, my_snils):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = get_table(soup)
    snils_list = get_snils_list(table)
    my_place = get_my_place_by_snils_list(snils_list, my_snils)

    accepts_before_me = count_accepts_before_me(table, my_place)

    return str(my_place), str(accepts_before_me)

def count_accepts_before_me(table,my_place):
    lines = table.find_all('tr')[:my_place]
    accepts = my_place-1
    for i in range(1,len(lines)):
        try:
            if lines[i].attrs['class']==['notagree']:
                accepts-=1
        except: pass
    return accepts

def get_number_of_budget_places(driver):
    return str(driver.find_element_by_id('tab').find_element_by_tag_name('span').text)


def get_snils_list(table):
    return table.find_all('nobr')

def get_all_of_my_places(nums_of_down_clicks = info.num_of_down_clicks, my_snils = info.my_snils_for_MAI, directions = info.directions_of_MAI):
    return_my_places = ''
    driver = make_driver()
    numdir = 0
    choose_options(driver)
    for num in tqdm(nums_of_down_clicks):
        choose_the_option(driver, 'spec_select', num)
        time.sleep(.5)

        my_place, accepts_before_me = get_my_place_and_accepts_before_me(driver, my_snils)
        return_my_places += directions[numdir] + ' [Бюджетных мест:' + get_number_of_budget_places(driver) + ']\n   Место:' + my_place + '\n'+ '   Согласий выше:' + accepts_before_me + '\n'
        numdir+=1
        time.sleep(.1)
    driver.quit()
    return return_my_places

print(get_all_of_my_places())