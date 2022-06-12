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


def add_person_to_database(first_name, second_name, third_name, post_name, file_path):
    con = sqlite3.connect('database/face_recognition_db.db')
    cur = con.cursor()

    cur.execute(
        """
            INSERT INTO staff (first_name, second_name, third_name, post, file_path)
            VALUES (?, ?, ?, ?, ?);
        """, (first_name, second_name, third_name, post_name, file_path)
    )
    con.commit()

    cur.close()
    con.close()


def get_count_of_staff():
    con = sqlite3.connect('database/face_recognition_db.db')
    cur = con.cursor()

    cur.execute('SELECT COUNT(*) FROM staff;')
    value = cur.fetchall()
    result = value[0][0]

    cur.close()
    con.close()

    return result


def get_info_about_person(user_id):
    con = sqlite3.connect('database/face_recognition_db.db')
    cur = con.cursor()

    cur.execute(f'SELECT * FROM staff WHERE staff_id="{user_id}";')
    value = cur.fetchall()

    result = value[0]

    cur.close()
    con.close()

    return result
