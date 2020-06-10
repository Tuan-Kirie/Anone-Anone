import psycopg2


class Database:
    def __init__(self):
        self.con = psycopg2.connect('dbname=anoneanone user=postgres password=301190')
