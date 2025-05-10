import logging

from requests import RequestException

from bs4 import BeautifulSoup

from constants import RESPONSE_ENCODING
from exceptions import PageLoadError, ParserFindTagException


def get_response(session, url, encoding=RESPONSE_ENCODING):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException:
        raise PageLoadError(url)


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def fetch_and_parse(session, url):
    """Получает страницу по URL и парсит её с помощью BeautifulSoup."""
    response = get_response(session, url)
    return BeautifulSoup(response.text, features='lxml')
