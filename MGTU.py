import fitz
import requests
import info
from tqdm import tqdm
import os

def download_pdf(url):
    list_page = requests.get(url)
    pdf_file = open(r'list-file.pdf', 'wb')
    pdf_file.write(list_page.content)
    pdf_file.close()

def get_num_of_start_page(pdf_file):
    number_of_pages = pdf_file.pageCount
    start_phrase = 'Поступающие на места в рамках КЦП по общему конкурсу'
    for page_num in range(number_of_pages):
        page = pdf_file.loadPage(page_num)
        page_txt = page.getText()
        start_symbol = page_txt.find(start_phrase)
        if start_symbol !=-1:
            return page_num, start_symbol

def get_snils_list(pdf_file, num_of_start_page,start_symbol):
    number_of_pages = pdf_file.pageCount
    snils_list = pdf_file.loadPage(num_of_start_page).getText()[start_symbol:].split('\n')[25:]
    for page_num in range(num_of_start_page+1, number_of_pages):
        page_snils_list = pdf_file.loadPage(page_num).getText().split('\n')[24:]
        snils_list += page_snils_list
    return snils_list

def get_my_place(snils_list, my_snils):
    for place in range(len(snils_list)//11):
        if snils_list[place*11 +1 ] == my_snils: return snils_list[place*11]
    return -1

def remove_forecast(snils_list_with_forecast):
    snils_list = []
    for row in snils_list_with_forecast:
        if len(row) == 14 or 1<=len(row)<=5 : snils_list.append(row)
        elif len(row) == 18:
            snils_list.append(row[:3])
            snils_list.append(row[4:])
        elif len(row) == 19:
            snils_list.append(row[:4])
            snils_list.append(row[5:])
    return snils_list

def get_number_of_budget_places(pdf_file, num_of_start_page, start_symbol):
    number_of_budget_places = pdf_file.loadPage(num_of_start_page).getText()[start_symbol+55:start_symbol+55+3]
    return number_of_budget_places

def get_accepts_before_me(snils_list, my_place):
    number_of_rows = int(my_place)
    accepts_before_me=0
    for row in range(number_of_rows):
        if snils_list[row*11+ 10] == 'Да': accepts_before_me+=1
    return accepts_before_me

def get_my_place_and_accepts(url, my_snils):
    download_pdf(url)
    pdf_file = fitz.open('list-file.pdf')
    num_of_start_page, start_symbol = get_num_of_start_page(pdf_file)
    snils_list_with_forecast = get_snils_list(pdf_file, num_of_start_page, start_symbol)
    snils_list = remove_forecast(snils_list_with_forecast)
    my_place = get_my_place(snils_list, my_snils)

    accepts_before_me = get_accepts_before_me(snils_list, my_place)
    number_of_budget_places = get_number_of_budget_places(pdf_file, num_of_start_page, start_symbol )
    return str(my_place), str(accepts_before_me), str(number_of_budget_places)

def get_all_of_my_places(my_snils = info.my_snils_for_MGTU, dirrection_pdfs= info.MGTU_PDFs, directions_names = info.directions_of_MGTU):
    places = ''
    for num_dir in tqdm(range(3)):
        my_place, accepts_before_me, number_of_budget_places = get_my_place_and_accepts(dirrection_pdfs[num_dir], my_snils)
        places += directions_names[num_dir]+ '[Бюджетных мест:'+ number_of_budget_places + ']:\n   Место:' + my_place + '\n   Согласий Выше:' + accepts_before_me+'\n'
    os.remove('list-file.pdf')
    return places
print(get_all_of_my_places())