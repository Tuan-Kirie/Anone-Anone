import os
import time
import requests
import re
import urllib.request
import cfscrape
import random
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import literal
from sqlalchemy.sql import select


class Preview:
    def __init__(self, url, proxy):
        """
        :type proxy: HTTP proxy object
        """
        self.url = url
        self.cookies = {"mature": "c3a2ed4b199a1a15f5a5483504c7a75a7030dc4bi%3A1%3B"}
        self.soup = self.get_soup_to_parse().content
        self.proxy = proxy

    def take_url(self):
        if 'https://' in self.url:
            return self.url
        else:
            raise print('Введена недействительная ссылка')

    def get_soup_to_parse(self):
        while True:
            try:
                page = requests.get(self.url, cookies=self.cookies)
                soup = BeautifulSoup(page.content, 'html.parser')
                return soup
            except requests.RequestException:
                print('Не удалось открыть страницу, попытка использовать прокси')
                try:
                    page = requests.get(self.url, cookies=self.cookies, proxy=self.proxy)
                    print('Удалось открыть страницу с прокси')
                except Exception:
                    continue
            soup = BeautifulSoup(page.content, 'html.parser')
            if (soup is not None) and len(soup) > 0:
                return soup
            else:
                print('Не удалось спарсить суп')
            time.sleep(10)


class Db:
    DRIVER = 'postgresql+psycopg2://'
    HOST = '@127.0.0.1:'
    PORT = '5432'
    DB_NAME = '/anoneanone'
    NAME = 'postgres'
    PASSWORD = '301190'

    def __init__(self):
        self.metadata = MetaData()
        self.engine = self.connect(self.HOST, self.PORT, self.DB_NAME, self.NAME, self.PASSWORD, self.DRIVER)
        self.ranobe = self.get_tables(self.engine, 'ranobe_ranobe')
        self.author_table = self.get_tables(engine=self.engine, type='ranobe_author')
        self.ranobe_table = self.get_tables(engine=self.engine, type='ranobe_ranobe')
        self.publisher_table = self.get_tables(engine=self.engine, type='ranobe_publisher')
        self.typeof_table = self.get_tables(engine=self.engine, type='ranobe_typeof')
        self.year_table = self.get_tables(engine=self.engine, type='ranobe_year')
        self.status_of_table = self.get_tables(engine=self.engine, type='ranobe_status')
        self.genres_table = self.get_tables(engine=self.engine, type='ranobe_genres')
        self.tags_table = self.get_tables(engine=self.engine, type='ranobe_tags')
        self.ranobe_tags_table = self.get_tables(engine=self.engine, type='ranobe_ranobe_tags')
        self.ranobe_genres_table = self.get_tables(engine=self.engine, type='ranobe_ranobe_genre')
        self.chapter_table = self.get_tables(engine=self.engine, type='ranobe_chapter')
        # db vars
        self.session = Session(bind=self.engine)
        self.con = self.engine.connect()

    def connect(self, host, port, db_name, name, password, driver):
        try:
            engine = create_engine(driver + name + ':' + password + host + port + db_name)
        except Exception:
            raise print('Не удалось подключиться к дб')
        return engine

    def get_tables(self, engine, type):
        table = Table(type, self.metadata, autoload=True, autoload_with=engine)
        return table

    def engine_c(self):
        self.engine = self.connect(self.HOST, self.PORT, self.DB_NAME, self.NAME, self.PASSWORD, self.DRIVER)
        return self.engine


class DBTitle(Db):
    def __init__(self, author, year, description, alternate_name,
                 title_id, status_of, publisher, type_of,
                 genres, tags, title_name):
        Db.__init__(self)
        self.title_name = title_name
        self.author = author
        self.genres = genres
        self.tags = tags
        self.publisher = publisher
        self.type_of = type_of
        self.year = year
        self.status_of = status_of
        self.title_id = title_id
        self.description = description
        self.alternate_name = alternate_name
        self.ranobe_id = self.insert_ranobe()
        self.inserted_tags = self.insert_ranobe_tags()
        self.inserted_genres = self.insert_ranobe_genre()

    def check(self, table_name, check_column, check_arg):
        check = self.session.query(literal(True)).filter(
            self.session.query(table_name)
                .filter(check_column == check_arg)
                .exists()) \
            .scalar(
        )
        if check is True:
            return True
        else:
            return False

    def insert_author(self):
        if self.check(self.author_table, self.author_table.c.author, self.author):
            selecter = select([self.author_table.c.id]).where(self.author_table.c.author == self.author)
            result = self.session.execute(selecter)
            return result.first()[0]
        else:
            selecter = self.author_table.insert().values(author=self.author)
            result = self.session.execute(selecter)
            self.session.commit()
            return result.inserted_primary_key[0]

    def insert_genres(self):
        result = []
        for k in self.genres:
            if self.check(self.genres_table, self.genres_table.c.genre, k):
                selecter = select([self.genres_table.c.id]).where(self.genres_table.c.genre == k)
                result.append(self.session.execute(selecter).first()[0])
            else:
                insert = self.genres_table.insert().values(genre=k)
                result_ex = self.session.execute(insert)
                self.session.commit()
                result.append(result_ex.inserted_primary_key[0])
        return result

    def insert_tags(self):
        result = []
        for tag in self.tags:
            if self.check(self.tags_table, self.tags_table.c.tag, tag):
                selecter = select([self.tags_table.c.id]).where(self.tags_table.c.tag == tag)
                result.append(self.session.execute(selecter).first()[0])
            else:
                insert = self.tags_table.insert().values(tag=tag)
                result_ex = self.session.execute(insert)
                self.session.commit()
                result.append(result_ex.inserted_primary_key[0])
        return result

    def insert_publisher(self):
        if self.check(self.publisher_table, self.publisher_table.c.publisher, self.publisher):
            selecter = select([self.publisher_table.c.id]).where(self.publisher_table.c.publisher == self.publisher)
            result = self.session.execute(selecter)
            return result.first()[0]
        else:
            insert = self.publisher_table.insert().values(publisher=self.publisher)
            result = self.session.execute(insert)
            self.session.commit()
            return result.inserted_primary_key[0]

    def insert_ranobe_genre(self):
        to_com = []
        checker = self.check(self.ranobe_table, self.ranobe_table.c.title, self.title_name)
        if len(self.insert_genres()) > 0 and checker is not True:
            for genre in self.insert_genres():
                insert = self.ranobe_genres_table.insert().values(genres_id=genre, ranobe_id=self.ranobe_id)
                result = self.session.execute(insert)
                to_com.append(result)
            return to_com
        else:
            return False

    def insert_ranobe_tags(self):
        to_com = []
        checker = self.check(self.ranobe_table, self.ranobe_table.c.title, self.title_name)
        if len(self.insert_tags()) > 0 and checker is not True:
            for tag_id in self.insert_tags():
                insert = self.ranobe_tags_table.insert().values(tags_id=tag_id, ranobe_id=self.ranobe_id)
                result = self.session.execute(insert)
                to_com.append(result)
            return to_com
        else:
            return False

    def insert_status(self):
        if self.check(self.status_of_table, self.status_of_table.c.status, self.status_of):
            selecter = select([self.status_of_table.c.id]).where(self.status_of_table.c.status == self.status_of)
            result = self.session.execute(selecter)
            return result.first()[0]
        else:
            insert = self.status_of_table.insert().values(status=self.status_of)
            result = self.session.execute(insert)
            self.session.commit()
            return result.inserted_primary_key[0]

    def insert_typeof(self):
        if self.check(self.typeof_table, self.typeof_table.c.type_of, self.type_of):
            selecter = select([self.typeof_table.c.id]).where(self.typeof_table.c.type_of == self.type_of)
            result = self.session.execute(selecter)
            return result.first()[0]
        else:
            insert = self.typeof_table.insert().values(type_of=self.type_of)
            result = self.session.execute(insert)
            self.session.commit()
            return result.inserted_primary_key[0]

    def insert_year(self):
        if self.check(self.year_table, self.year_table.c.year, self.year):
            selecter = select([self.year_table.c.id]).where(self.year_table.c.year == self.year)
            result = self.session.execute(selecter)
            return result.first()[0]
        else:
            insert = self.year_table.insert().values(year=int(self.year))
            result = self.session.execute(insert)
            self.session.commit()
            return result.inserted_primary_key[0]

    def insert_ranobe(self):
        if self.check(self.ranobe_table, self.ranobe_table.c.title, self.title_name):
            selecter = select([self.ranobe_table.c.id]).where(self.ranobe_table.c.title == self.title_name)
            result = self.session.execute(selecter)
            return result.first()[0]
        else:
            insert = self.ranobe_table.insert().values(title_id=self.title_id,
                                                       title=self.title_name,
                                                       description=self.description,
                                                       alternate_name=self.alternate_name,
                                                       author_id=self.insert_author(),
                                                       pub_year_id=self.insert_year(),
                                                       publisher_id=self.insert_publisher(),
                                                       status_id=self.insert_status())
            result = self.session.execute(insert)
            self.session.commit()
            return result.inserted_primary_key[0]



class InsertChapter(Db):
    def __init__(self, text, chapter_name, ranobe_id):
        Db.__init__(self)
        self.paragraph = text
        self.chapter_name = chapter_name
        self.ranobe_id = ranobe_id
        self.chapter_id = self.insert_chapter()

    def check(self, table_name, check_column, check_arg):
        check = self.session.query(literal(True)).filter(
            self.session.query(table_name)
                .filter(check_column == check_arg)
                .exists()) \
            .scalar(
        )
        if check is True:
            return True
        else:
            return False

    def insert_chapter(self):
        if self.check(self.chapter_table, self.chapter_table.c.chapter_name, self.chapter_name):
            selecter = select([self.chapter_table.c.id]).where(self.chapter_table.c.chapter_name == self.chapter_name)
            result = self.session.execute(selecter)
            return result.first()[0]
        else:
            insert = self.chapter_table.insert().values(chapter_name=self.chapter_name,
                                                        paragraph_text=self.paragraph,
                                                        ranobe_id=self.ranobe_id)
            result = self.session.execute(insert)
            self.session.commit()
            return result.inserted_primary_key[0]


class SearchPage(Preview):
    def __init__(self, url, proxy):
        Preview.__init__(self, url, proxy)
        self.url = url
        self.soup = self.get_soup_to_parse()
        self.next_page = self.get_next_page_link()
        self.titles = self.parse_titles_of_page()
        self.descriptions = self.parse_descriptions_of_page()
        self.boofer = []
        self.vosk = self.titles_of_search()
        self.title_page_list = self.boofer

    def get_next_page_link(self):
        next_page_link = self.soup.select_one('li.next a')
        if next_page_link is None:
            print('Не удалось найти ссылку на след стр')
            raise ('Остановка по причине отсутствия след страницы для парсинга')
        return 'https://tl.rulate.ru' + next_page_link['href']

    def parse_titles_of_page(self):
        parsed_title_list = self.soup.select('ul.search-results > li > p > a')
        return parsed_title_list

    def parse_descriptions_of_page(self):
        title_descriptions_list = self.soup.select('div.tooltip_templates')
        return title_descriptions_list

    def titles_of_search(self):
        for k in range(len(self.titles)):
            self.boofer.append({'title_name': self.titles[k].string,
                                'description': self.descriptions[k].string,
                                'link': 'https://tl.rulate.ru' + self.titles[k]['href']})


class TitlePage(Preview):

    def __init__(self, url, dictionary, proxy):
        Preview.__init__(self, url, proxy)
        self.title_soup = self.get_soup_to_parse()
        self.dictionary = dictionary
        self.title_name = self.parse_dict()[0]
        self.description = self.parse_dict()[1]
        self.title_info = self.parse_info_block()
        self.author = self.title_info[0]
        self.publisher = self.title_info[1]
        self.year = self.title_info[2]
        self.status_of = self.title_info[3]
        self.count_of_chapters = self.title_info[4]
        self.alternate_name = self.title_info[5]
        self.genres = self.parse_genres_of_title()
        self.tags = self.parse_tags_of_title()
        self.chapter_links = self.parse_links_to_text()
        self.type_of = 'Новеллы и ранобэ'
        self.image_url = self.get_title_image()
        self.dictionary = dictionary

    @staticmethod
    def check(string):
        if string == 'Доступ запрещен':
            return True
        else:
            return False

    def parse_dict(self):
        name_title = self.dictionary.get('title_name')
        description = self.dictionary.get('description')
        link = self.dictionary.get('link')
        return name_title, description, link

    def get_title_image(self):
        title_image_url = self.title_soup.select_one('div.slick > div > img')['src']
        image_url = 'https://tl.rulate.ru' + title_image_url
        return image_url

    def parse_info_block(self):
        info_block = self.title_soup.find_all('p')
        author, publisher, year, status_of, count_of_chapters, alternate_name \
            = 'Неизвестно', 'Неизвестно', 0, False, 0, 'Неизвестно'
        i = 0
        while i < len(info_block):
            if 'Автор:' in info_block[i].getText():
                author_boof = str(info_block[i].getText())
                author = author_boof.replace('Автор: ', '')
            elif 'Издательство:' in info_block[i].getText():
                publisher_boof = str(info_block[i].getText())
                publisher = publisher_boof.replace('Издательство: ', '')
            elif 'Год выпуска:' in info_block[i].getText():
                year_boofer = str(info_block[i].getText())
                if len(year_boofer) > 3:
                    year = [int(s) for s in str.split(year_boofer) if s.isdigit()]
                    if year is None or len(year) == 0:
                        year = 2000
                    else:
                        year = year[0]
                elif year_boofer is None or len(year_boofer) <= 3:
                    year = 0
                else:
                    year = 0
            elif 'Произведение имеет возрастное ограничение 18+' in info_block[i].getText():
                status_of = True
            elif 'Количество глав:' in info_block[i].getText():
                count_of_chapters_boofer = str(info_block[i].getText())
                count_of_chapters = count_of_chapters_boofer.replace('Количество глав: ', '')
            elif 'Альтернативное название:' in info_block[i].getText():
                alternate_name_boofer = str(info_block[i].getText())
                alternate_name = alternate_name_boofer.replace('Альтернативное название: ', '')
            i += 1
        return author, publisher, year, status_of, count_of_chapters, alternate_name

    def parse_genres_of_title(self):
        genres_loc = self.title_soup.find_all(href=re.compile("genre"))
        boof = []
        for k in genres_loc:
            boof.append(k.string)
        return boof

    def parse_tags_of_title(self):
        tags_loc = self.title_soup.find_all(href=re.compile("tag"))
        boof = []
        for k in tags_loc:
            boof.append(k.string)
        return boof

    def parse_links_to_text(self):
        boof = []
        avialable_block = self.title_soup.select('a[class="btn btn-small btn-info"]')
        for k in range(len(avialable_block)):
            boof.append('https://tl.rulate.ru' + avialable_block[k].get('href'))
        return boof


class ChapterPage(Preview):
    def __init__(self, url, proxy):
        Preview.__init__(self, url, proxy)
        self.soup = self.get_soup_to_parse()
        self.name = self.parse_chapter_name()
        self.text_container = self.parse_text()

    def check_chapter(self):
        pass

    def parse_chapter_name(self):
        chapter_name = self.soup.find('h1').string
        return chapter_name

    def parse_text(self):
        text_chapter = self.soup.select('div.content-text > p')
        texter = ''
        for k in text_chapter:
            texter += str(k)
        return texter




class ImageParse:
    def __init__(self, id, img_url):
        self.abs_path = 'C:\\Users\\Hikari\\Documents\\Pon-pon\\silfi\\static\\ponpon\\titles'
        self.id = id
        self.url = img_url

    def create_img_directory(self):
        try:
            os.makedirs(self.abs_path + r'\\' + str(self.id))
        except FileExistsError:
            pass

    def download_img_to_destpath(self):
        try:
            urllib.request.urlretrieve(self.url, self.abs_path + r'\\'
                                       + str(self.id) + r'\\' + str(self.id) + '.jpg')
            print('Логотип ранобэ скачана - id ====' + self.id)
        except Exception or OSError:
            print('Не удалось скачать логотип ранобэ')


if __name__ == "__main__":
    search_url = 'https://tl.rulate.ru/search/?cat=2'
    parsed_ranobes = 0
    print("Парсим прокси")
    proxy = None
    print("Прокси спаршено")
    while True:
        proxy_r = None #{'html': proxy.checked_proxy[random.randrange(0, 7)]}
        print('Используется прокси  --------', proxy_r)

        print('Подготовка......')
        search_page = SearchPage(search_url, proxy_r)
        print('страница открыта')
        i = 0
        title_id = 1000
        while i < len(search_page.title_page_list):
            title_page = TitlePage(url=search_page.boofer[i]['link'],
                                   dictionary=search_page.title_page_list[i],
                                   proxy=proxy_r)
            print('страница спаршена')

            insert_ranobe = DBTitle(author=title_page.author,
                                    year=title_page.year,
                                    description=title_page.description,
                                    alternate_name=title_page.alternate_name,
                                    title_id=title_id,
                                    status_of=title_page.status_of,
                                    publisher=title_page.publisher,
                                    type_of=title_page.type_of,
                                    genres=title_page.genres,
                                    tags=title_page.tags,
                                    title_name=title_page.title_name)
            print('ранобэ добавлено в базу')
            try:
                print('Парсим логотип ранбоэ')
                image = ImageParse(insert_ranobe.ranobe_id, title_page.image_url)
                image.create_img_directory()
                image.download_img_to_destpath()
                print('Логотип успешно скачан')
            except urllib.request.HTTPError or OSError:
                pass
            for page in title_page.chapter_links:
                chapter_page = ChapterPage(page, proxy_r)
                name = chapter_page.name
                print('спаршена глава с названием ---', name)
                if chapter_page.check_chapter() is True:
                    continue
                else:
                    text = chapter_page.text_container
                    insert_db = InsertChapter(chapter_name=name,
                                              ranobe_id=insert_ranobe.ranobe_id,
                                              text=text)
            i += 1
            title_id += 1
            parsed_ranobes += 1
            del title_page
            print('Ранобе спаршено, всего --', parsed_ranobes)
        search_url = search_page.next_page
        del search_page