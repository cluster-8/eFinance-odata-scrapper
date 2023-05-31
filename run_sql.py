import db

file = "/home/vv/Downloads/tarifas.sql"

def insert(sql_string):
    try:
        conn = db.get_database_psql()
        cur = conn.cursor()
        cur.execute(sql_string)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f'Insert query error: {e}')

with open(file) as f:
    for line in f:
        insert(line)
