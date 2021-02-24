import sqlite3
import re

conn = sqlite3.connect('news.db')

class Sqldb:

    def r_users(user_f):

        id = user_f[0]

        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute("SELECT uid FROM main ORDER BY uid")
        prow = cursor.fetchall()

        for och in prow:
            prow = re.sub(r"[(,)]","",str(prow))

        if str(user_f[0]) not in prow:

            with conn:
                cursor = conn.cursor()
                #cursor.execute('INSERT INTO user(uid, name) VALUES (?, ?)', (user_f))
                cursor.execute('INSERT INTO main(uid,uname) VALUES (?,?)', (user_f))

                cursor.close()
                return False
        else:
            with conn:

                cursor.close()
            return True

    def p_chanel(id):

        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute("SELECT uid FROM main WHERE uid = ?", (id,))
        mem = cursor.fetchall()

        for och in mem:
            mem = re.sub(r"[(,)]","",str(mem))

        if str(id) not in mem:
            cursore.close()
            return False
        else:
            cursor = conn.cursor()
            cursor.execute('SELECT utgrup, ungrup FROM main WHERE uid = ?', (id,))
            mem = cursor.fetchall()
            cursor.close()

            return mem[0]

    def addchanel_sql(chanid, userid):

        conn = sqlite3.connect('new.db')
        cursor = conn.cursor()
