import sqlite3
import re

class Sqldb:
    def get_max_grup():
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute("SELECT seq FROM sqlite_sequence WHERE name = ?",('grup',))
        prow = cursor.fetchall()
        prow = Sqldb.och(prow[0])
        prow = Sqldb.ochstr(prow)
        cursor.close()
        return prow

    def get_param(id):

        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        znach = []
        peremen = ['g_username','g_users', 'g_last']
        for i in peremen:
            zapros = "SELECT " + i + " FROM grup WHERE id = ?"
            cursor.execute(zapros,(id,))
            znach.append(cursor.fetchall())
        for i in range(len(znach)):
            znach[i] = Sqldb.ochstr(znach[i])

        get = {'title': znach[0], 'last_news': znach[2], 'users': znach[1].split()}
        # prow = Sqldb.och(prow)
        cursor.close()
        return get

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
            cursor.close()
            return False
        else:
            cursor = conn.cursor()
            cursor.execute('SELECT utgrup, ungrup FROM main WHERE uid = ?', (id,))
            mem = cursor.fetchall()
            cursor.close()

            return mem[0]

    def add_new_grup(grup):
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute("SELECT g_id FROM grup WHERE g_id = ?",(grup['id'],))
        prow = cursor.fetchall()

        if prow != []:
            prow = Sqldb.och(prow[0])
        else:
            prow = Sqldb.och(prow)

        if str(grup['id']) not in prow:
            with conn:
                cursor = conn.cursor()

                cursor.execute('INSERT INTO grup(g_id, g_title, g_username, g_last, g_users) VALUES (?,?,?,?,?)',
                (grup['id'],grup['title'],grup['username'], grup['last'], grup['u_id']))
                cursor.execute('SELECT ugroup FROM main WHERE uid = ?',(grup['u_id'],))

                prow = cursor.fetchall()
                prow = Sqldb.och(prow[0])


                if str(grup['id']) not in prow:
                    prow = Sqldb.ochstr(str(prow))
                    prow = (prow + " " + str(grup['id']))
                    if prow is None:
                        prow = grup['id']
                    print(str(grup['id']) + ";;" + str(prow))
                    # prow = prow + " " + grup["u_id"]
                    prow = Sqldb.ochstr(str(prow))
                    cursor.execute('UPDATE main SET ugroup = ? WHERE uid = ?',(prow,grup['u_id'],))

                cursor.close()
                return True
        else:
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT g_users FROM grup WHERE g_id = ?", (grup['id'],))
                prow = cursor.fetchall()

                prow = Sqldb.och(prow[0])

                if str(grup['u_id']) not in prow:
                    prow = Sqldb.ochstr(str(prow))
                    prow = (prow + " " + str(grup['u_id']))
                    # prow = Sqldb.och(prow[0]
                    if prow is None:
                        prow = grup['u_id']

                    cursor = conn.cursor()
                    prow = Sqldb.ochstr(str(prow))
                    cursor.execute('UPDATE grup SET g_users = ? WHERE g_id = ?',(prow,grup['id'],))
                    cursor.execute('SELECT ugroup FROM main WHERE uid = ?',(grup['u_id'],))

                    prow = cursor.fetchall()

                    prow = Sqldb.och(prow)

                    if str(grup['id']) not in prow:

                        prow = Sqldb.ochstr(str(prow))
                        prow = (prow + " " + str(grup['id']))

                        if prow is None:
                            prow = grup['id']

                        prow = Sqldb.ochstr(str(prow))

                        cursor.execute('UPDATE main SET ugroup = ? WHERE uid = ?',(prow,grup['u_id'],))

                    cursor.close()
                    return True
                else:
                    cursor.close()
                    return False

    def grup_plus(id):
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute("SELECT utgrup FROM main WHERE uid = ?", (id,))
        prow = cursor.fetchall()
        prow = Sqldb.och(prow[0])
        prow = Sqldb.ochstr(prow)


        with conn:
            cursor.execute('UPDATE main SET utgrup =? WHERE uid = ?',(int(prow)+1,id,))
        cursor.close()
        return True

    def och(prow):
        for och in prow:
            prow = re.sub(r"[\[\](,)']","",str(prow))
            prow = prow.split()
        if not prow:
            prow = []
        return prow

    def ochstr(prow):
        prow = re.sub(r"[\[\](,)']","",str(prow))
        return prow
