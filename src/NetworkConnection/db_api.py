import sqlite3


def create_db(db_name):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        print("DB is connected")
        with open("schema.sql", "r") as f:
            schema = f.read()
            cur.executescript(schema)
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

def set_user_online(db_name, table, fio):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        query = "UPDATE " + table + " SET online = 1 WHERE fio =?;"
        cur.execute(query, (fio,))
        cur.close()
        conn.commit()

def set_user_offline(db_name, table, fio):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        if fio == "":
            query = "UPDATE " + table + " SET online = 0;"
            cur.execute(query)
        else:
            query = "UPDATE " + table + " SET online = 0 WHERE fio =?;"
            cur.execute(query, (fio,))
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


def get_users_online(db_name, table):
    with sqlite3.connect(db_name) as conn:
        print(table)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        query = f'SELECT fio, public_key FROM {table} WHERE online = 1;'
        cur.execute(query)
        users = cur.fetchall()
        cur.close()
        return users


def find_by_fio(db_name, table, fio):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        query = "SELECT id, fio, public_key FROM " + table + " WHERE fio = ?"
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
        query = "SELECT count(id) as cnt FROM " + table + " WHERE online = 1;"
        cur.execute(query)
        resp = cur.fetchone()
        cur.close()
        return resp["cnt"]


def add_election(db_name, question, amount):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        print("add_election")
        cur.execute("INSERT INTO elections (question) VALUES (?)", (question,))
        cur.close()


def find_by_question(db_name, question):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        print("find_by_question")
        cur.execute("SELECT id, amount FROM elections WHERE question = ?", (question,))
        resp = cur.fetchall()
        cur.close()
        return resp

def get_valid_election(db_name):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT question FROM elections WHERE id = (SELECT MAX(id) FROM elections)")
        resp = cur.fetchone()
        print(resp["question"])
        cur.close()
        return resp["question"]


def add_user_vote(db_name, table, fio, question, vote):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        print(fio + "   " + question + "   " + vote)
        users = find_by_fio(db_name, "voters", fio)
        user = users[0]
        elections = find_by_question(db_name, question)
        election = elections[0]

        query = "INSERT INTO " + table + " (id_voter, id_election, vote) VALUES (?, ?, ?)"
        cur.execute(query, (user["id"], election["id"], vote))
        cur.close()
        print("successfully add user voice")


def count_votes(db_name, question):
    with sqlite3.connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        elections = find_by_question(db_name, question)
        election = elections[0]


        cur.execute("SELECT count(vote) as total FROM voters_elections_link WHERE id_election = ?", (election["id"],))
        total = cur.fetchone()["total"]
        
        print(f'total {total}')
        cur.execute("SELECT count(vote) as true FROM voters_elections_link WHERE vote = 'true' AND id_election = ?", (election["id"], ))
        true = cur.fetchone()["true"]
        print(f'true {true}')

        cur.execute("""UPDATE elections SET amount = ?,
                    results_true = ?
                    WHERE id = ?""", (total, true, election["id"]))
        conn.commit()
        cur.close()
        return true / total, (total - true) / total
        
