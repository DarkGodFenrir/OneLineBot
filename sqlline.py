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

    def edit_number(l_id,param):
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        with conn:
            cursor.execute('UPDATE grup SET g_last = ? WHERE g_username = ?',(l_id, str(param['title']),))
        cursor.close()

    def get_param(id):

        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        znach = []
        peremen = ['g_username','g_users', 'g_last', 'g_title']
        for i in peremen:
            zapros = "SELECT " + i + " FROM grup WHERE id = ?"
            cursor.execute(zapros,(id,))
            znach.append(cursor.fetchall())
        for i in range(len(znach)):
            znach[i] = Sqldb.ochstr(znach[i])
        get = {'title': znach[0], 'last_news': znach[2], 'users': znach[1].split(),
        'nazv': znach[3]}
        # prow = Sqldb.och(prow)
        cursor.close()
        return get

    def get_us_param(id):
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        znach = []
        peremen = ['refers','balans']
        for i in peremen:
            zapros = "SELECT " + i + " FROM main WHERE uid = ?"
            cursor.execute(zapros,(id,))
            znach.append(cursor.fetchall())
        for i in range(len(znach)):
            znach[i] = Sqldb.ochstr(znach[i])
        get = {
        'refers': znach[0],
        'balans': znach[1]}
        # prow = Sqldb.och(prow)
        cursor.close()
        return get

    def get_grup_param(id):
        per = False
        if (str(id).find("_p") > -1):
            id = re.sub("[_p]","",id)
            per = True

        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        znach = []
        peremen = ['g_username','g_id', 'g_title']
        for i in peremen:
            zapros = "SELECT " + i + " FROM grup WHERE g_id = ?"
            cursor.execute(zapros,(id,))
            znach.append(cursor.fetchall())
        for i in range(len(znach)):
            znach[i] = Sqldb.ochstr(znach[i])

        get = {
        'title': znach[0],
        'g_id': znach[1],
        'nazv': znach[2]}
        if per:
            get['g_id'] = str(get['g_id']) + "_p"
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

    def edit_list(param):
        conn = sqlite3.connect('news.db')
        paus = False
        for_r = 3
        print(str(param) + " param")
        cursor = conn.cursor()
        if param[2] != 'p':
            cursor.execute("SELECT ugroup FROM main WHERE uid = ?", (param[2],))
        else:
            cursor.execute("SELECT ugroup FROM main WHERE uid = ?", (param[3],))
            paus = True
        prow = cursor.fetchall()
        prow = Sqldb.all_och(prow)
        prow = prow.split()
        print(str(prow )+ "3")
        if str(param[0]) == "del":
            if param[1] in prow:
                prow.remove(param[1])
                cursor.execute("SELECT g_users FROM grup WHERE g_id = ?", (param[1],))
                grup_u = cursor.fetchall()
                grup_u = Sqldb.all_och(grup_u)
                grup_u = grup_u.split()
                if param[2] in grup_u:
                    grup_u.remove(param[2])

                cursor.execute("SELECT utgrup FROM main WHERE uid = ?", (param[2],))
                min_grup = cursor.fetchall()
                min_grup = Sqldb.all_och(min_grup)
                min_grup = int(min_grup) - 1
                prow = Sqldb.all_och(prow)
                grup_u = Sqldb.all_och(grup_u)
                with conn:
                    cursor = conn.cursor()
                    cursor.execute('UPDATE main SET ugroup = ?, utgrup = ? WHERE uid = ?',(prow, min_grup, param[2],))
                    cursor.execute('UPDATE grup SET g_users = ? WHERE g_id = ?',(grup_u,param[1],))
                    for_r = 0
                    cursor.close()

            elif paus:
                if str(param[1]+"_p") in prow:
                    prow.remove(str(param[1]) + "_p")
                    cursor.execute("SELECT utgrup FROM main WHERE uid = ?", (param[3],))
                    min_grup = cursor.fetchall()
                    min_grup = Sqldb.all_och(min_grup)
                    min_grup = int(min_grup) - 1
                    prow = Sqldb.all_och(prow)
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute('UPDATE main SET ugroup = ?, utgrup = ? WHERE uid = ?',(prow, min_grup, param[3],))
                        for_r = 0
                        cursor.close()

        elif str(param[0]) == "pau":
            for i in range(len(prow)):
                if str(prow[i]) == str(param[1]):
                    prow[i] = str(prow[i]) + "_p"

            print(prow)
            cursor.execute("SELECT g_users FROM grup WHERE g_id = ?", (param[1],))
            grup_u = cursor.fetchall()
            grup_u = Sqldb.all_och(grup_u)
            grup_u = grup_u.split()
            if param[2] in grup_u:
                grup_u.remove(param[2])
            prow = Sqldb.all_och(prow)
            grup_u = Sqldb.all_och(grup_u)
            print(prow)
            print(grup_u)
            with conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE main SET ugroup = ? WHERE uid = ?',(prow, param[2],))
                cursor.execute('UPDATE grup SET g_users = ? WHERE g_id = ?',(grup_u,param[1],))
                for_r = 1
                cursor.close()

        elif str(param[0]) == "beg":
            for i in range(len(prow)):
                if str(prow[i]) == str(param[1]+"_p"):
                    prow[i] = str(param[1])

            print(prow)
            cursor.execute("SELECT g_users FROM grup WHERE g_id = ?", (param[1],))
            grup_u = cursor.fetchall()
            grup_u = Sqldb.all_och(grup_u)
            grup_u = grup_u.split()
            if param[3] not in grup_u:
                grup_u.append(param[3])
            prow = Sqldb.all_och(prow)
            grup_u = Sqldb.all_och(grup_u)
            print(prow)
            print(grup_u)
            with conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE main SET ugroup = ? WHERE uid = ?',(prow, param[3],))
                cursor.execute('UPDATE grup SET g_users = ? WHERE g_id = ?',(grup_u,param[1],))
                for_r = 2
                cursor.close()

        return for_r

    def add_ref(inviter):
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute('SELECT refers FROM main WHERE uid = ?',(inviter,))
        inv = cursor.fetchall()
        inv = int(Sqldb.all_och(inv))
        inv += 1
        with conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE main SET refers = ? WHERE uid = ?',(inv, inviter,))
        if inv%2 == 0 and inv != 0:
            with conn:
                cursor.execute('SELECT ungrup FROM main WHERE uid = ?',(inviter,))
                grup = cursor.fetchall()
                grup = int(Sqldb.all_och(grup))
                grup += 1
                cursor = conn.cursor()
                cursor.execute('UPDATE main SET ungrup = ? WHERE uid = ?',(grup, inviter,))
            cursor.close()
            return True
        else:
            cursor.close()
            return False


    def get_grup(id):
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ugroup FROM main WHERE uid = ?", (id,))
        prow = cursor.fetchall()
        prow = Sqldb.och(prow[0])
        prow = Sqldb.ochstr(prow)
        cursor.close()
        return prow

    def get_user():
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute("SELECT uid FROM main WHERE akt = 1")
        prow = cursor.fetchall()
        prow = Sqldb.all_och(prow[0])
        cursor.close()
        return prow

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

    def all_och(par):
        if len(par) == 1:
            par = Sqldb.och(par[0])
        par = Sqldb.ochstr(par)
        return par


    def ochstr(prow):
        prow = re.sub(r"[\[\](,)']","",str(prow))
        return prow
