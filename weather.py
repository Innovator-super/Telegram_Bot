import requests
from bs4 import BeautifulSoup
APPID = 'your_appid'
def weathering(x, y):
    url = f'https://yandex.ru/pogoda/ru-RU/details'
    response = requests.get(url, params = {'lat' : x, 'lon' : y}, headers = {'X-Yandex-Weather-Key': APPID})
    web_page = response.text
    soup = BeautifulSoup(web_page, "lxml")
    all = soup.find_all('div', attrs = {'style':'border:0;clip:rect(0 0 0 0);clip-path:inset(50%);height:1px;margin:0 -1px -1px 0;overflow:hidden;padding:0;position:absolute;width:1px;white-space:nowrap'})
    url1 = f'https://yandex.ru/weather'
    response1 = requests.get(url1, params = {'lat' : x, 'lon' : y}, headers = {'X-Yandex-Weather-Key': APPID})
    web_page1 = response1.text
    soup1 = BeautifulSoup(web_page1, "lxml")
    all1 = soup1.find_all('span', attrs = {'class':'temp__value temp__value_with-unit'})
    all2 = soup1.find_all('div', attrs = {'class':'link__condition day-anchor i-bem'})
    all3 = soup1.find_all('div', attrs = {'class':'term term_orient_h fact__feels-like'})
    all4 = soup1.find_all('p', attrs = {'class':'maps-widget-fact__title'})
    return f'''{all1[0].text} {all2[0].text}. {all3[0].text}.
{all4[0].text}

{all[0].text}
{all[1].text}
{all[2].text}
{all[3].text}'''
def weather_(city):
    url = f'https://yandex.ru/pogoda/ru-RU/{city}/details?lang=ru&via=mf#21'
    response = requests.get(url, headers = {'X-Yandex-Weather-Key': APPID})
    web_page = response.text
    soup = BeautifulSoup(web_page, "lxml")
    all = soup.find_all('div', attrs = {'style':'border:0;clip:rect(0 0 0 0);clip-path:inset(50%);height:1px;margin:0 -1px -1px 0;overflow:hidden;padding:0;position:absolute;width:1px;white-space:nowrap'})
    url1 = f'https://yandex.ru/weather/{city}'
    response1 = requests.get(url1, headers = {'X-Yandex-Weather-Key': APPID})
    web_page1 = response1.text
    soup1 = BeautifulSoup(web_page1, "lxml")
    all1 = soup1.find_all('span', attrs = {'class':'temp__value temp__value_with-unit'})
    all2 = soup1.find_all('div', attrs = {'class':'link__condition day-anchor i-bem'})
    all3 = soup1.find_all('div', attrs = {'class':'term term_orient_h fact__feels-like'})
    all4 = soup1.find_all('p', attrs = {'class':'maps-widget-fact__title'})
    return f'''{all1[0].text} {all2[0].text}. {all3[0].text}.
{all4[0].text}

{all[0].text}
{all[1].text}
{all[2].text}
{all[3].text}'''