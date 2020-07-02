from classes import SearchPage, Database, TitlePage, ChapterPage, ImageParse, ProxyParser
from tqdm import tqdm

"""
Vars
"""
db = Database()
print('Starting parser, \nConnecting to db')
database = Database()
print('Database is connected \nParsing proxies')
proxy_parser = ProxyParser()
proxies = proxy_parser.find_page_data(proxy_parser.open_page())
print(f"Proxies parsed, total count = {len(proxies)}")
url = 'https://tl.rulate.ru/search/?cat=2'
"""
Main loop
"""
iteration = 1
while True:
    print(f'Starting parsing of search page\nParsing page = {iteration}')
    search_page = SearchPage(url, proxies)
    titles = search_page.parse_titles_of_page()
    descriptions = search_page.parse_descriptions_of_page()
    urls = [book_url['href'] for book_url in titles]
    print(f'Parsed total {len(titles)} titles\nStart parsing titles \n')
    with tqdm(total=(len(titles)), desc='Titles') as pbar:
        for x in range(len(titles)):
            pbar.update(x)
            title_page = TitlePage('https://tl.rulate.ru' + urls[x], proxies)
            title_name = titles[x].string
            title_description = descriptions[x].string
            title_info = title_page.parse_info_block()
            chapter_names, chapter_urls = title_page.parse_available_chapters()
            ranobe_id = database.check_ranobe_existing(title_name)
            if ranobe_id:
                for i in range(len(chapter_names)):
                    if database.chapter_existing(ranobe_id, chapter_names[i]):
                        continue
                    else:
                        chapter_page = ChapterPage(chapter_urls[i], proxies)
                        chapter_name = chapter_page.parse_chapter_name()
                        chapter_text = chapter_page.parse_chapter_text()
                        database.insert_chapter(ranobe_id, chapter_name, chapter_text)
            else:
                if title_info.get('author') is None:
                    author = None
                else:
                    author = database.insert_author(title_info.get('author'))
                if title_info.get('publisher') is None:
                    publisher = None
                else:
                    publisher = database.insert_publisher(title_info.get('publisher'))
                genres_tags = title_page.parse_genres_and_tags()
                added_ran_id = database.insert_ranobe(title_name, title_description, None, author,
                                                      publisher, title_info.get('alternate'),
                                                      title_info.get('adult_status'))
                img = ImageParse(added_ran_id, title_page.parse_title_image(), proxies)
                img_path = img.download_img_to_dest_path()
                database.update_ranobe_img(added_ran_id, img_path)
                genres = database.insert_genres(genres_tags[0])
                database.insert_ranobe_genres(added_ran_id, genres)
                tags = database.insert_tags(genres_tags[1])
                database.insert_ranobe_tags(added_ran_id, tags)
                for k in range(len(chapter_names)):
                    chapter_page = ChapterPage(chapter_urls[k], proxies)
                    chapter_name = chapter_page.parse_chapter_name()
                    chapter_text = chapter_page.parse_chapter_text()
                    database.insert_chapter(added_ran_id, chapter_name, chapter_text)
    url = search_page.get_next_page_link()
    iteration += 1
