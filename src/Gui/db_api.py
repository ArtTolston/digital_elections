import sqlite3

def create_db(db_name):
    with sqlite3.connect(db_name) as conn:
	    cur = conn.cursor()
	    print("DB is connected")
	    create_table_query1 = '''CREATE TABLE voters (
	                            idv INTEGER PRIMARY KEY AUTOINCREMENT,
	                            fio TEXT NOT NULL,
	                            public_key BLOB NOT NULL,
	                            );'''
	    cur.execute(create_table_query)
	    cur.close()
	    conn.commit()