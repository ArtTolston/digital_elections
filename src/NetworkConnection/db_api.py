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
        cur.execute("CREATE TABLE current_voters (\
                    fio TEXT PRIMARY KEY,\
                    public_key BLOB NOT NULL);")
        cur.close()
        conn.commit()


def add_user(db_name, table, fio, public_key):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        print(f"Add user {fio}, {public_key}")
        query = "INSERT INTO " + table + " (fio, public_key) VALUES (?, ?);"
        cur.execute(query, (fio, public_key))
        cur.close()
        conn.commit()


def get_users(db_name, table):
    with sqlite3.connect(db_name) as conn:
        print(table)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        query = f'SELECT fio, public_key FROM {table} ;'
        cur.execute(query)
        users = cur.fetchall()
        cur.close()
        return users


def find_by_fio(db_name, table, fio):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT fio, public_key FROM ? WHERE fio = ?", (table, fio))
        users = cur.fetchall()
        if not users:
            print("no such user, mudak blyat'")
        cur.close()
        return users
