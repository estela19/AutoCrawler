import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os, sys, subprocess

date = str(datetime.now())
date = date[:date.rfind(':')].replace(' ', '_')
date = date.replace(':', 'H') + 'M'

query = input('Search keyword : ')
query = query.replace(' ', '+')

news_num = int(input('How many news(only num) : '))

news_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}'

req = requests.get(news_url.format(query))
soup = BeautifulSoup(req.text, 'html.parser')


news_dict = {}
idx = 0
cur_page = 1

print('crawling...')

while idx < news_num:
    table = soup.find('ul',{'class' : 'list_news'})
    li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
    area_list = [li.find('div', {'class':'news_area'}) for li in li_list]
    a_list = [area.find('a', {'class': 'news_tit'}) for area in area_list]

    for n in a_list[:min(len(a_list), news_num-idx)]:
        news_dict[idx] = {'title': n.get('title'), 'url': n.get('href')}
        idx += 1

    cur_page += 1

    pages = soup.find('div', {'class': 'sc_page_inner'})
    next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page)][0].get('href')

    req = requests.get('https://search.naver.com/search.naver' + next_page_url)
    soup = BeautifulSoup(req.text, 'html.parser')


print("Crawling Success")

print("Data Converting..")
news_df = DataFrame(news_dict).T

folder_path = os.getcwd()
xlsx_file_name = '네이버뉴스_{}_{}.xlsx'.format(query, date)

news_df.to_excel(xlsx_file_name)

print('Excel Save Success | dir : {}\\{}'.format(folder_path, xlsx_file_name))