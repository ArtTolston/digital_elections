import sqlite3


def create_db(db_name):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        print("DB is connected")
        create_table_query = '''CREATE TABLE voters (
                                fio TEXT PRIMARY KEY,
                                public_key BLOB NOT NULL
                                );'''
        cur.execute(create_table_query)
        cur.execute("CREATE TABLE current_voters (\
                    fio TEXT PRIMARY KEY,\
                    public_key BLOB NOT NULL);")
        cur.execute("CREATE TABLE election (\
                    question TEXT PRIMARY KEY,\
                    amount INTEGER NOT NULL,\
                    valid TEXT NOT NULL,\
                    results_true INTEGER,\
                    results_false INTEGER);")
        cur.execute("CREATE TABLE voices (\
                    fio TEXT NOT NULL,\
                    question TEXT NOT NULL,\
                    voice TEXT NOT NULL,\
                    PRIMARY KEY (fio, question),\
                    FOREIGN KEY (fio) REFERENCES voters(fio),\
                    FOREIGN KEY (question) REFERENCES election(question));")
        cur.close()
        conn.commit()


def add_user(db_name, table, fio, public_key):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        print(f"Add user {fio}, {public_key}")
        query = "INSERT INTO " + table + " (fio, public_key) VALUES (?, ?);"
        cur.execute(query, ( fio, public_key))
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
        query = "SELECT fio, public_key FROM " + table + " WHERE fio = ?"
        cur.execute(query, (fio, ))
        users = cur.fetchall()
        if not users:
            print("no such user, mudak blyat'")
        cur.close()
        return users


def get_number_of_voters(db_name, table):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        query = "SELECT count(fio) as cnt FROM " + table + ";"
        cur.execute(query)
        resp = cur.fetchone()
        cur.close()
        return resp["cnt"]


def add_election(db_name, question, amount):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        print("add_election")
        cur.execute("INSERT INTO election (question, amount, valid) VALUES (?, ?, ?)", (question, amount, "yes"))
        cur.close()

def get_valid_election(db_name):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT question FROM election WHERE valid = 'yes' LIMIT 1")
        resp = cur.fetchone()
        print(resp["question"])
        cur.close()
        return resp["question"]
