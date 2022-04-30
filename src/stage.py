import requests
import config
from bs4 import BeautifulSoup as bs


def get_tracking_code(url, h, d) -> str:
    """получает промежуточный системный код"""
    temp = requests.post(url=url, headers=h, data=d, allow_redirects=False)
    if temp.status_code == 303:
        tracker = temp.headers['Location']
        return tracker
    else:
        return False

def get_html(tracking_link, headers) -> str:
    """возвращает html домашней страницы пользователя"""
    temp = requests.get(tracking_link, headers)
    if temp.status_code == 200:
        return temp.text
    else:
        raise False

def get_person(soup) -> list:
    """парсит ФИ пользователя"""
    cl = 'color-gray text-shadow-white'
    person_row = soup.find_all('span', class_=cl)
    st = str(person_row[0].get_text())
    num = ''.join(list(filter(lambda a: a != '\n' and a != ' ', st)))
    num = num.split(',')[0]
    name = str(person_row[1].get_text())
    person = [num, name]
    return person

def get_status(soup) -> str:
    """парсит статус пользователя"""
    def filter_status(stat_row) -> str:
        very_row = str(stat_row).split()
        return ' '.join(very_row)
    cl = 'span8 text-shadow-white'
    stat_row = soup.find('div', class_=cl).get_text()
    stat = filter_status(stat_row)
    return stat

def stage(num, email):
    """получить статус пользоввателя на портале"""
    URL = config.URL
    HEADERS = config.HEADERS
    par = {
        'registrationNumber': num,
        'email': email
    }

    code = get_tracking_code(URL, HEADERS, par)
    if code:
        tracking_link = URL+get_tracking_code(URL, HEADERS, par)

        ht = get_html(tracking_link, HEADERS)
        if ht:
            soup = bs(ht, 'html.parser')
            tags = ['number', 'name', 'stage']
            values = [*get_person(soup), get_status(soup)]
            result = dict(zip(tags, values))
            return result
        else:
            return False
    else:
        return False
