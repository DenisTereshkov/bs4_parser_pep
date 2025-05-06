import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    EXPECTED_STATUS,
    MAIN_DOC_URL,
    PEP_MAIN_URL,
    PEPS_NUMERICAL_URL
)
from outputs import control_output
from utils import get_response, find_tag


def pep(session):
    response = get_response(session, PEPS_NUMERICAL_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    tr_tag = soup.find_all('tr')
    results = [('Статус', 'Количество')]
    actual_statuses = {}
    total_peps = len(tr_tag) - 1
    for i in tqdm(range(1, len(tr_tag))):
        table_pep_status = find_tag(tr_tag[i], 'abbr').text[1:]
        expected_status = EXPECTED_STATUS[table_pep_status]
        pep_link = urljoin(PEP_MAIN_URL, tr_tag[i].a['href'])
        response = get_response(session, pep_link)
        soup = BeautifulSoup(response.text, 'lxml')
        pep_card_dl_tag = find_tag(
            soup,
            'dl',
            {'class': 'rfc2822 field-list simple'}
        )
        for tag in pep_card_dl_tag:
            if tag.name == 'dt' and tag.text == 'Status:':
                pep_card_status = tag.next_sibling.next_sibling.string
                if pep_card_status not in actual_statuses:
                    actual_statuses[pep_card_status] = 0
                actual_statuses[pep_card_status] += 1
                if pep_card_status not in expected_status:
                    logging.info(
                        f'Несовпадающие статус для:{pep_link}\n'
                        f'Статус в карточке: {pep_card_status}\n'
                        f'Статус в общей таблице: {expected_status}'
                    )
    for status in actual_statuses:
        results.append((status, actual_statuses[status]))
    results.append(('Total', total_peps))
    return results


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')

    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'}
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.text.replace('\n', ' ')
        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session):
    response = session.get(MAIN_DOC_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Не найден список c версиями Python')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = session.get(downloads_url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features='lxml')
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag,
        'a',
        {'href': re.compile(r'.+pdf-a4\.zip')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


MODE_TO_FUNCTION = {
    'pep': pep,
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    yp_table = PrettyTable()
    main()
