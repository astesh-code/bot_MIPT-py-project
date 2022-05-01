import config as conf
import requests

from bs4 import BeautifulSoup as bs


def get_tracking_code(url: str, h: dict, d: dict) -> str:
    """
    получает промежуточный системный код. 
    url: ссылка получения кода
    h: HEADERS html-запроса
    d: BODY html-запроса
    """
    temp = requests.post(url=url, headers=h, data=d, allow_redirects=False)
    if temp.status_code == conf.post_success:
        tracker = temp.headers[conf.header_with_code]
        return tracker
    else:
        return False


def get_html(tracking_link: str, headers: dict) -> str:
    """
    возвращает html домашней страницы пользователя
    tracking_url: ссылка получения кода
    h: HEADERS html-запроса 
    """
    temp = requests.get(tracking_link, headers)
    if temp.status_code == conf.get_success:
        return temp.text
    else:
        raise False


def get_person(soup: bs) -> list:
    """
    парсит ФИ пользователя
    soup: bs-объект полученный из html-страницы пользователя
    """
    person_row = soup.find_all("span", class_=conf.class_with_name)
    st = str(person_row[0].get_text())
    num = "".join(list(filter(lambda a: a != "\n" and a != " ", st)))
    num = num.split(",")[0]
    name = str(person_row[1].get_text())
    person = [num, name]
    return person


def get_status(soup: bs) -> str:
    """
    парсит статус пользователя
    soup: bs-объект полученный из html-страницы пользователя
    """
    def filter_status(stat_row) -> str:
        very_row = str(stat_row).split()
        return " ".join(very_row)
    stat_row = soup.find("div", class_=conf.get_success).get_text()
    stat = filter_status(stat_row)
    return stat


def stage(num: str, email: str) -> dict:
    """
    получить статус пользоввателя на портале
    num: индивидуальный номер участника в формате "ABC-12354/78"
    """
    URL = conf.URL
    HEADERS = conf.HEADERS
    par = {
        conf.number_site_name: num,
        conf.email_site_name: email
    }

    code = get_tracking_code(URL, HEADERS, par)
    if code:
        tracking_link = URL+get_tracking_code(URL, HEADERS, par)

        ht = get_html(tracking_link, HEADERS)
        if ht:
            soup = bs(ht, "html.parser")
            tags = ["number", "name", "stage"]
            values = [*get_person(soup), get_status(soup)]
            result = dict(zip(tags, values))
            return result
        else:
            return None
    else:
        return None
