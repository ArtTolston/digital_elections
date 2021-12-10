import sqlite3


def create_db(db_name):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        print("DB is connected")
        create_table_query = '''CREATE TABLE voters (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                fio TEXT NOT NULL,
                                public_key BLOB NOT NULL
                                );'''
        cur.execute(create_table_query)
        cur.close()
        conn.commit()


def add_user(db_name, fio, public_key):
    with sqlite3.connect(db_name) as conn:
    	cur = conn.cursor()
    	print(f"Add user {fio}, {public_key}")
    	cur.execute("INSERT INTO voters (fio, public_key) VALUES (?, ?)", (fio, public_key))
    	cur.close()
    	conn.commit()


def get_users(db_name):
    with sqlite3.connect(db_name) as conn:
    	conn.row_factory = sqlite3.Row
    	cur = conn.cursor()
    	cur.execute("SELECT fio, public_key FROM voters")
    	users = cur.fetchall()
    	cur.close()
    	return users
