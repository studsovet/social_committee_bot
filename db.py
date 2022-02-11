import sqlite3
import datetime

path_to_db = 'database.db'


def get_connection():
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS "applications" 
                ( "id" INTEGER, "date" INTEGER, "chat_id" TEXT, "campus" TEXT, 
                "problem_area" TEXT, "problem" TEXT, "contact" TEXT, "text_problem" TEXT, 
                "language" INTEGER, PRIMARY KEY("id") )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS "users" ( "id" INTEGER, "chat_id" INTEGER, "name" TEXT, 
                "username" TEXT, "language" TEXT, PRIMARY KEY("id") )''')
    conn.commit()
    return cur, conn




def add_data_in_applications(chat_id, column, data):
    cur, conn = get_connection()
    # cur.execute("SELECT {} from applications WHERE chat_id = '{}' "
    #             "AND date = (SELECT MAX(date) from applications)".format(column, chat_id))
    # data = cur.fetchone()[0] + data
    cur.execute("UPDATE applications SET {} = '{}' WHERE chat_id = '{}' "
                "AND date = (SELECT MAX(date) from applications WHERE chat_id = '{}')".format(column, data, chat_id,
                                                                                              chat_id))
    conn.commit()
    cur.close()


def get_data_from_applications(chat_id, column):
    cur, conn = get_connection()
    cur.execute("SELECT {} from applications WHERE chat_id = '{}' "
                "AND date = (SELECT MAX(date) from applications WHERE chat_id = '{}')".format(column, chat_id, chat_id))
    ans = cur.fetchone()
    print(ans, chat_id, column)
    ans = ans[0]
    cur.close()
    return ans


def get_data_from_users(chat_id, column):
    cur, conn = get_connection()
    cur.execute("SELECT {} from users WHERE chat_id = '{}'".format(column, chat_id))
    ans = cur.fetchone()[0]
    cur.close()
    return ans


def create_application_in_db(chat_id):
    cur, conn = get_connection()
    cur.execute("INSERT INTO applications (chat_id, date) VALUES (?, ?)", (chat_id, datetime.datetime.now()))
    conn.commit()
    cur.close()


def create_user_in_db(chat_id, name, username):
    cur, conn = get_connection()
    cur.execute("SELECT * from users WHERE chat_id = {}".format(chat_id))
    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO users (chat_id, name, username) VALUES (?, ?, ?)", (chat_id, name, username))
        conn.commit()
    cur.close()


def get_count_applications():
    cur, conn = get_connection()
    cur.execute("SELECT id from applications WHERE id = (SELECT MAX(id) from applications)")
    ans = cur.fetchone()[0]
    cur.close()
    return ans


def add_text_in_applications(chat_id, column, data):
    cur, conn = get_connection()
    cur.execute("SELECT {} from applications WHERE chat_id = '{}' "
                "AND date = (SELECT MAX(date) from applications WHERE chat_id = '{}')".format(column, chat_id, chat_id))
    a = cur.fetchone()[0]
    cur.close()
    cur, conn = get_connection()
    if a is not None:
        data = a + '\n' + data
    cur.execute("UPDATE applications SET {} = '{}' WHERE chat_id = '{}' "
                "AND date = (SELECT MAX(date) from applications WHERE chat_id = '{}')".format(column, data, chat_id,
                                                                                              chat_id))
    conn.commit()
    cur.close()


def clear_cell(chat_id, table, column):
    cur, conn = get_connection()
    cur.execute("UPDATE {} SET {} = NULL WHERE chat_id = '{}' "
                "AND date = (SELECT MAX(date) from applications WHERE chat_id = '{}')".format(table, column, chat_id,
                                                                                              chat_id))
    conn.commit()
    cur.close()


def get_time_application(chat_id):
    cur, conn = get_connection()
    cur.execute("SELECT MAX(date) from applications WHERE chat_id = '{}'".format(chat_id))
    return cur.fetchone()[0]
