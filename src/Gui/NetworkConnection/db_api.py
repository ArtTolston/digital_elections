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
		add_user_query = f'''INSERT INTO voters (fio, public_key) VALUES ({fio}, {public_key});'''
		cur.execute(add_user_query)
		cur.close()
		conn.commit()


def get_users(db_name):
	with sqlite3.connect(db_name) as conn:
		cur = conn.cursor()
		add_user_query = f'''SELECT fio, public_key FROM voters;'''
		cur.execute(add_user_query)
		users = cur.fetchall()
		cur.close()
		return users

