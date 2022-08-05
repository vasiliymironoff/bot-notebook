import sqlite3
from optparse import Option
from typing import List, Tuple, Union

from data import Note


class Database:
    def __init__(self):
        self.con = sqlite3.connect('notebook.db')
        self.cur = self.con.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        sql = """\
        CREATE TABLE IF NOT EXISTS user (
            telegram_id INTEGER  PRIMARY KEY 
        );
        CREATE TABLE IF NOT EXISTS category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            name_category TEXT,
            FOREIGN KEY (telegram_id) REFERENCES user(telegram_id)
        );
        CREATE TABLE IF NOT EXISTS note (
            note_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            category_id INTEGER,
            title TEXT,
            text TEXT,
            photo TEXT,
            date_created TEXT,
            FOREIGN KEY (telegram_id) REFERENCES user(telegram_id),
            FOREIGN KEY (category_id) REFERENCES category(category_id)
        );
        """
        with self.con:
            self.cur.executescript(sql)

    def create_user(self, telegram_id: int) -> None:
        with self.con:
            self.cur.execute("INSERT INTO user (telegram_id) VALUES(?)", (telegram_id,))

    def select_all_telegram_id(self) -> List[str]:
        return [i[0] for i in self.cur.execute('SELECT telegram_id FROM user').fetchall()]

    def select_name_category(self, telegram_id) -> List[str]:
        sql = '''\
            SELECT name_category 
            FROM user
                 INNER JOIN category USING(telegram_id)
            WHERE telegram_id = ?
        '''
        return [i[0] for i in self.cur.execute(sql, (telegram_id,)).fetchall()]

    def select_note(self, telegram_id: int, title: str) -> Union[Note, None]:
        data = {'telegram_id': telegram_id, 'title': title}
        sql = '''\
            SELECT note_id, name_category, title, text, photo 
            FROM note
                 INNER JOIN category USING(category_id)
            WHERE note.telegram_id = :telegram_id  AND title = :title
        '''
        res = self.cur.execute(sql, data).fetchone()
        if res is not None:
            return Note(*res)
        return None

    def select_notes(self, telegram_id: int) -> List[Note]:
        data = {'telegram_id': telegram_id}
        sql = '''\
            SELECT note_id, name_category, title, text, photo 
            FROM note
                 INNER JOIN category USING(category_id)
            WHERE note.telegram_id = :telegram_id'''
        return [Note(*i) for i in self.cur.execute(sql, data)]

    def select_title(self, telegram_id) -> List[str]:
        res = self.cur.execute('SELECT title FROM note WHERE telegram_id = (?)', (telegram_id, )).fetchall()
        return [i[0] for i in res]

    def insert_note(self, data: dict) -> None:
        with self.con:
            self.cur.execute('INSERT INTO note (telegram_id, category_id, title, text, photo)\
                              VALUES (:telegram_id, :category_id, :title, :text, :photo)', data)

    def insert_category(self, data: dict) -> None:
        with self.con:
            self.cur.execute('INSERT INTO category (telegram_id, name_category)\
                              VALUES (:telegram_id, :name_category)', data)
