from requests.exceptions import MissingSchema
from sqlalchemy import MetaData, create_engine, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class Database:
    DRIVER = 'postgresql+psycopg2://'
    HOST = '@127.0.0.1:'
    PORT = '5432'
    DB_NAME = '/anoneanone'
    NAME = 'postgres'
    PASSWORD = '301190'

    def __init__(self):
        """
        special database vars
        """
        self.engine = self.connect()
        self.session = Session(bind=self.engine)
        self.metadata = MetaData(bind=self.engine)
        self.metadata.reflect(bind=self.engine)
        """
        tables
        """
        self.author_table = self.metadata.tables['ranobe_author']
        self.ranobe_table = self.metadata.tables['ranobe_ranobe']
        self.publisher_table = self.metadata.tables['ranobe_publisher']
        self.year_table = self.metadata.tables['ranobe_year']
        self.genres_table = self.metadata.tables['ranobe_genres']
        self.tags_table = self.metadata.tables['ranobe_tags']
        self.ranobe_tags_table = self.metadata.tables['ranobe_ranobe_tags']
        self.ranobe_genres_table = self.metadata.tables['ranobe_ranobe_genres']
        self.chapter_table = self.metadata.tables['ranobe_chapters']

    def connect(self):
        """
        mini function to connect to db
        :return: engine
        :raise: SystemExit
        """
        try:
            return create_engine(self.DRIVER + self.NAME + ':' +
                                 self.PASSWORD + self.HOST + self.PORT + self.DB_NAME)
        except SQLAlchemyError as e:
            print(e)
            raise SystemExit(1)

    def check_ranobe_existing(self, ranobe_name):
        """
        special function for check existing var on table
        :param ranobe_name:
        :return: if var exists True else False
        """
        check = self.session.query(self.ranobe_table).filter_by(name=ranobe_name).scalar()
        return check if check is not None else False

    def chapter_existing(self, ranobe_id, chapter_name):
        check = self.session.query(self.chapter_table).filter_by(chapter_name=chapter_name,
                                                                 ranobe_id=ranobe_id).scalar()
        return True if check is None else False

    def __check_author_existing(self, author):
        if author is None:
            return False
        else:
            check = self.session.query(self.author_table).filter_by(author=author).scalar()
            return check

    def insert_author(self, author):
        author_checked = self.__check_author_existing(author)
        if author_checked is None:
            try:
                add = self.author_table.insert().values(author=author)
                res = self.session.execute(add).inserted_primary_key[0]
                self.session.commit()
                return res
            except SQLAlchemyError as e:
                print(e)
                self.session.rollback()
                return None
        else:
            return None

    def __check_publisher_existing(self, publisher):
        if publisher is None:
            return False
        else:
            check = self.session.query(self.publisher_table).filter_by(publisher=publisher).scalar()
            return check

    def insert_publisher(self, publisher):
        check = self.__check_publisher_existing(publisher)
        if check is None:
            try:
                add = self.publisher_table.insert().values(publisher=publisher)
                res = self.session.execute(add).inserted_primary_key[0]
                self.session.commit()
                return res
            except SQLAlchemyError as e:
                print(e)
                self.session.rollback()
                return None
        else:
            return None

    def insert_ranobe(self, name, description, image, author_id, publisher_id, alternate_name, adult_status):
        insert = self.ranobe_table.insert().values(name=name,
                                                   description=description,
                                                   image=image,
                                                   author_id=author_id,
                                                   publisher_id=publisher_id,
                                                   alternate_name=alternate_name,
                                                   adult_status=adult_status)
        try:
            result = self.session.execute(insert)
            self.session.commit()
            return result.inserted_primary_key[0]
        except SQLAlchemyError as e:
            print('Any problems with inserting ranobe')
            print(e)
            return False

    def update_ranobe_img(self, ranobe_id, img_path):
        if img_path is not None and ranobe_id is not None:
            try:
                upd = update(self.ranobe_table).where(self.ranobe_table.c.id == ranobe_id). \
                    values(image=img_path)
                self.session.execute(upd)
                self.session.commit()
            except (SQLAlchemyError, MissingSchema) as e:
                print('Cant update img of ranobe with path = ' + img_path)
                print(e)

    def insert_chapter(self, ranobe_id, chapter_name, chapter_text):
        insert = self.chapter_table.insert().values(
            chapter_name=chapter_name,
            text=chapter_text,
            ranobe_id=ranobe_id
        )
        try:
            result = self.session.execute(insert)
            self.session.commit()
            return result.inserted_primary_key[0]
        except SQLAlchemyError as e:
            print("any problems with inserting chapter ")
            print(e)
            return False

    def __check_genre_tag_exist(self, genres=None, tags=None):
        if genres is not None:
            return [self.session.query(self.genres_table).
                        filter_by(genre=genres[i]).scalar() for i in range(len(genres))]
        elif tags is not None:
            return [self.session.query(self.tags_table).
                        filter_by(tag=tags[i]).scalar() for i in range(len(tags))]
        else:
            return False

    def insert_genres(self, genres):
        if genres is None:
            return
        checked_genres = self.__check_genre_tag_exist(genres)
        for i in range(len(checked_genres)):
            if checked_genres[i] is None and checked_genres is not False:
                try:
                    add = self.genres_table.insert().values(genre=genres[i])
                    res = self.session.execute(add).inserted_primary_key[0]
                    self.session.commit()
                    checked_genres[i] = res
                except SQLAlchemyError as e:
                    print(e)
                    self.session.rollback()
                    continue
            else:
                continue
        return checked_genres

    def insert_tags(self, tags):
        if tags is None:
            return
        checked_tags = self.__check_genre_tag_exist(tags)
        for i in range(len(checked_tags)):
            if checked_tags[i] is None or checked_tags is not False:
                try:
                    add = self.tags_table.insert().values(tag=tags[i])
                    res = self.session.execute(add).inserted_primary_key[0]
                    self.session.commit()
                    checked_tags[i] = res
                except SQLAlchemyError as e:
                    print(e)
                    self.session.rollback()
                    continue
            else:
                continue
        return checked_tags

    def insert_ranobe_tags(self, ranobe_id, tags):
        if tags is False:
            return
        else:
            for i in range(len(tags)):
                if tags[i] is None:
                    continue
                else:
                    try:
                        self.session.execute(self.ranobe_tags_table.insert().
                                             values(ranobe_id=ranobe_id, tags_id=tags[i]))
                    except SQLAlchemyError as e:
                        print('Cant add tag with ranobe')
                        print(e)
                        continue

    def insert_ranobe_genres(self, ranobe_id, genres):
        if genres is False:
            return
        else:
            for i in range(len(genres)):
                if genres[i] is None:
                    continue
                else:
                    try:
                        self.session.execute(self.ranobe_genres_table.insert().
                                             values(ranobe_id=ranobe_id, genres_id=genres[i]))
                    except SQLAlchemyError as e:
                        print('Cant add genre with ranobe')
                        print(e)
                        continue


if __name__ == "__main__":
    pass

# def __check_genre_or_tag_exist(self, flag, data):
#     buffer = []
#     filtered_buffer = []
#     if flag is self.genres_table:
#         buffer = [self.session.query(self.genres_table).filter_by(genre=x).scalar() for x in data]
#     elif flag is self.tags_table:
#         buffer = [self.session.query(self.tags_table).filter_by(tag=x).scalar() for x in data]
#     for i in range(len(buffer)):
#         if buffer[i] is None:
#             try:
#                 if flag is self.genres_table:
#                     insert = self.session.execute(flag.insert().values(genre=data[i])).inserted_primary_key[0]
#                 else:
#                     insert = self.session.execute(flag.insert().values(tag=data[i])).inserted_primary_key[0]
#                 self.session.commit()
#                 filtered_buffer.append(insert)
#             except SQLAlchemyError as e:
#                 self.session.rollback()
#                 print(e)
#         else:
#             filtered_buffer.append(buffer[i])
#     return filtered_buffer
#
# def insert_genres_tags(self, ranobe_id, genres, tags):
#     if tags is not None and len(tags) > 0:
#         tags_b = self.__check_genre_or_tag_exist(self.tags_table, tags)
#         for tag in tags_b:
#             try:
#                 add = self.ranobe_tags_table.insert().values(ranobe_id=ranobe_id, tags_id=tag)
#                 self.session.execute(add)
#                 self.session.commit()
#             except SQLAlchemyError as e:
#                 print(e)
#     elif genres is not None and len(genres) > 0:
#         genres_b = self.__check_genre_or_tag_exist(self.genres_table, genres)
#         for genre in genres_b:
#             try:
#                 add = self.ranobe_genres_table.insert().values(ranobe_id=ranobe_id, genres_id=genre)
#                 self.session.execute(add)
#                 self.session.commit()
#             except SQLAlchemyError as e:
#                 print(e)
