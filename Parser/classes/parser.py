import os
import re
import time
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup


def open_url(url, proxy=None):
    cookies = {'mature': 'c3a2ed4b199a1a15f5a5483504c7a75a7030dc4bi%3A1%3B'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    while True:
        try:
            return requests.get(url, cookies=cookies, headers=headers, timeout=5).content
        except (requests.exceptions.HTTPError, Exception):
            print("Attention connection problems, trying to use proxy")
            time.sleep(5)
            try:
                for i in range(len(proxy)):
                    return requests.get(url, proxies={'http': proxy[i]}, headers=headers, cookies=cookies, timeout=100).content
            except requests.exceptions.HTTPError:
                time.sleep(60)

class ProxyParser:
    PROXY_URL = 'https://free-proxy-list.net/'

    def __init__(self):
        self.session = HTMLSession()

    def open_page(self):
        request = self.session.get(self.PROXY_URL)
        request.html.render()
        return request.content

    @staticmethod
    def find_page_data(html):
        _proxies = []
        soup = BeautifulSoup(html, 'html.parser')
        ips = soup.select('tbody > tr > td:nth-child(1)')
        ports = soup.select('tbody > tr > td:nth-child(2)')
        for i in range(len(ips)):
            _proxies.append(f'{ips[i].string}:{ports[i].string}')
        return _proxies

    @staticmethod
    def check_proxies(proxy_list):
        _proxy_list = []
        for i in range(len(proxy_list)):
            request = requests.get('https://www.google.com/', proxies={"http": proxy_list[i]})
            if request.status_code == 200:
                _proxy_list.append({"http": proxy_list[i]})
            else:
                request = requests.get('https://www.google.com/', proxies={"https": proxy_list[i]})
                if request.status_code == 200:
                    _proxy_list.append({"https": proxy_list[i]})
                else:
                    pass
        return _proxy_list


class SearchPage:
    def __init__(self, url, proxy):
        self.soup = BeautifulSoup(open_url(url, proxy), 'html.parser')

    def get_next_page_link(self):
        next_page_link = self.soup.select_one('li.next a')
        if next_page_link is None:
            print('Cant find next page link')
            raise SystemExit(0)
        return 'https://tl.rulate.ru' + next_page_link['href']

    def parse_titles_of_page(self):
        parsed_title_list = self.soup.select('ul.search-results > li > p > a')
        return parsed_title_list

    def parse_descriptions_of_page(self):
        title_descriptions_list = self.soup.select('div.tooltip_templates')
        return title_descriptions_list


class TitlePage:
    def __init__(self, url, proxy):
        self.soup = BeautifulSoup(open_url(url, proxy), 'html.parser')

    def check_title_page(self):
        return False if self.soup.find('h1', text='Системная ошибка') or \
                        self.soup.find('h1', text='Доступ запрещен') else True

    def parse_info_block(self):
        author = self.soup.find_all('strong', text=re.compile('Автор:'))
        publisher = self.soup.find_all('strong', text=re.compile('Издательство:'))
        alternate = self.soup.find_all('strong', text=re.compile('Альтернативное название'))
        adult_status = self.soup.find_all('strong', text=re.compile('Произведение имеет возрастное ограничение 18'))
        buffer = {}
        try:
            auth_name = author[0].find_parent("p")
            buffer.update({'author': auth_name.em.string})
        except (AttributeError, IndexError):
            buffer.update({'author': None})
        try:
            publisher_name = publisher[0].find_parent("p")
            buffer.update({'publisher': publisher_name.em.string})
        except (AttributeError, IndexError):
            buffer.update({'publisher': None})
        try:
            alternate_name = alternate[0].find_parent('p')
            buffer.update({'alternate': alternate_name.em.string})
        except (AttributeError, IndexError):
            buffer.update({'alternate': None})
        try:
            buffer.update({'adult_status': True}) \
                if adult_status[0] is not None and len(adult_status) != 0 else buffer.update({'adult_status': False})
        except IndexError:
            buffer.update({'adult_status': False})
        return buffer

    def parse_available_chapters(self):
        buff_urls = []
        buff_names = []
        available = self.soup.select('a[class="btn btn-small btn-info"]')
        """
        need to early parse chapter names for check this existing without open chapter page
        """
        try:
            [buff_urls.append('https://tl.rulate.ru' + available[x].get('href')) for x in range(len(available))]
        except IndexError:
            print('No chapters available')
        try:
            [buff_names.append(available[x].find_parent().find_parent().find('td', {'class': 't'}).string) for x in
             range(len(available))]
        except (IndexError, IndexError):
            print('No names available')
        return buff_names, buff_urls

    def parse_genres_and_tags(self):
        genres_loc = self.soup.find_all(href=re.compile("genre"))
        tags_loc = self.soup.find_all(href=re.compile("tag"))
        try:
            genres_list = [x.string for x in genres_loc]
        except IndexError:
            genres_list = []
            print('No genres available')
        try:
            tags_list = [y.string for y in tags_loc]
        except IndexError:
            tags_list = []
            print('No tags available')
        return genres_list, tags_list

    def parse_title_image(self):
        try:
            imgage = self.soup.select_one('div.slick > div > img')['src']
        except TypeError as e:
            print(e)
            print('Image not found')
            return None
        return 'https://tl.rulate.ru' + imgage


class ChapterPage:
    def __init__(self, url, proxy):
        self.soup = BeautifulSoup(open_url(url, proxy), 'html.parser')

    def check_name(self):
        return True if self.soup.find('h1', text='Доступ запрещен') is None else False

    def parse_chapter_name(self):
        return self.soup.find('h1').string[16::]

    def parse_chapter_text(self):
        buffer = ''
        text = self.soup.select('div.content-text > p')
        for i in text:
            buffer += str(i)
        return buffer


class ImageParse:
    def __init__(self, id, img_url, proxy):
        self.abs_path = "C:\\Programming\\Anone-Anone\\backend\\media\\ranobe"
        self.id = id
        self.url = img_url

    def download_img_to_dest_path(self):
        if self.url is not None:
            try:
                image_data_bin = requests.get(self.url,
                                              headers={
                                                  'mature': 'c3a2ed4b199a1a15f5a5483504c7a75a7030dc4bi%3A1%3B'}).content
                with open(f"{self.abs_path}\\{str(self.id)}.jpg", "w+b") as data:
                    data.write(image_data_bin)
                return f"media\\ranobe\\{str(self.id)}.jpg"
            except TypeError:
                return 'media\\ranobe\\default.jpg'
        else:
            return 'media\\ranobe\\default.jpg'


