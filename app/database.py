import os
import psycopg2
from psycopg2.extras import RealDictCursor


class Database:

    def __init__(self):
        
        self.conn = psycopg2.connect(
        dbname="karibu",
        user="postgres",
        password="Alimanu195ogwal",
        host="localhost",
        port="5432"
        )
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        self.dict_cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        self.create_user_table()
        self.create_article_table()

        print("Connected to karibu")

    def create_user_table(self):
        user_table = "CREATE TABLE IF NOT EXISTS users(user_id serial PRIMARY KEY, \
            username varchar(50) UNIQUE, email varchar(30) UNIQUE, \
                password varchar(256), created_on TIMESTAMP DEFAULT NOW())"

        self.cur.execute(user_table)

    def create_article_table(self):
        article_table = "CREATE TABLE IF NOT EXISTS articles(article_id serial PRIMARY KEY, \
            title varchar(100), content varchar(3500), created_by varchar(50), created_on TIMESTAMP DEFAULT NOW())"

        self.cur.execute(article_table)

    