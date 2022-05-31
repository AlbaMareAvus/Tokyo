import sqlite3


def auth(login, password):
    con = sqlite3.connect('database/face_recognition_db.db')
    cur = con.cursor()

    # Check staff
    cur.execute(f'SELECT * FROM security WHERE login="{login}";')
    value = cur.fetchall()

    if value != [] and value[0][3] == password:
        result = True
    else:
        result = False

    cur.close()
    con.close()
    return result
