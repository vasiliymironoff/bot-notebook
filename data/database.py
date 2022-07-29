import sqlite3

from aiogram.dispatcher import FSMContext

con = None
cur = None


def start_db():
    global con, cur
    con = sqlite3.connect("notebook.db")
    cur = con.cursor()
    sql = """\
    CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER
    );
    CREATE TABLE IF NOT EXISTS category (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    );
    CREATE TABLE IF NOT EXISTS note (
        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category_id INTEGER,
        title TEXT,
        text TEXT,
        photo TEXT,
        date_created TEXT,
        hash TEXT,
        FOREIGN KEY (user_id) REFERENCES user(user_id),
        FOREIGN KEY (category_id) REFERENCES category(category_id)
    );
    """
    try:
        cur.executescript(sql)
    except sqlite3.DatabaseError as e:
        print("Ошибка:", e)
    else:
        con.commit()


def add_user_id(data):
    data['user_id'] = cur.execute("SELECT * FROM user WHERE telegram_id = :telegram_id", dict(data)).fetchall()[0][0]


def create_user(telegram_id):
    cur.execute("INSERT INTO user (telegram_id) VALUES(?)", (telegram_id,))
    con.commit()


def get_all_telegram_id():
    '''Возвращает спискок всех telegram_id пользователей, которые взаимодействовали с ботом'''
    return [i[0] for i in cur.execute('SELECT telegram_id FROM user').fetchall()]


def select_name_category(telegram_id):
    data = {'telegram_id': telegram_id}
    add_user_id(data)
    sql = '''\
        SELECT category_id, name 
        FROM user
             INNER JOIN category USING(user_id)
        WHERE user_id = :user_id
    '''
    return cur.execute(sql, data).fetchall()


def select_notes(telegram_id, title=None):
    data = {'telegram_id': telegram_id}
    add_user_id(data)
    sql = '''\
        SELECT name, title, text, photo 
        FROM note
             INNER JOIN category USING(category_id)
        WHERE note.user_id = :user_id '''
    if title is not None:
        sql += ' AND title = :title'
        data['title'] = title
    return cur.execute(sql, dict(data)).fetchall()


def select_title(telegram_id):
    data = {'telegram_id': telegram_id}
    add_user_id(data)
    return cur.execute('SELECT title FROM note WHERE user_id = :user_id', dict(data)).fetchall()


async def insert_note(state: FSMContext):
    async with state.proxy() as data:
        add_user_id(data)
        cur.execute('INSERT INTO note (user_id, category_id, title, text, photo)\
                     VALUES (:user_id, :category_id, :title, :text, :photo)', dict(data))
        con.commit()


async def insert_category(state: FSMContext):
    async with state.proxy() as data:
        add_user_id(data)
        cur.execute('INSERT INTO category (user_id, name)\
                     VALUES (:user_id, :name)', dict(data))
        con.commit()
