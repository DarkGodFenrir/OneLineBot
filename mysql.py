from contextlib import closing
import pymysql
import re
from pymysql.cursors import DictCursor

def connect():
    connection = pymysql.connect(
    host='localhost',
    user='root',
    password='12alex34',
    db='telegram_news',
    charset='utf8mb4',
    cursorclass=DictCursor)
    return connection

def obed(mem):
    stroka = ""
    for m in mem:
        stroka += m + " "
    return stroka

class Sqldb:
    def get_max_grup():
        prow = []
        with closing(connect()) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                                    SELECT
                                        id
                                    FROM
                                        grup
                                    WHERE
                                        g_role != -1
                                    AND
                                        g_users != ''
                                    """)
                for row in cursor:
                    prow.append(row['id'])
                return prow

    def edit_number(l_id,param):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                    query = "UPDATE grup SET g_last = {0} WHERE g_username = {1}"
                    query = query.format(l_id,param['title'])
                    cursor.execute(query)
                    conn.commit()

    def get_param(id):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                peremen = {
                            'gu': 'g_username', 'gus': 'g_users',
                            'gl': 'g_last', 'gt': 'g_title', 'id': id
                            }
                query = "SELECT {gu}, {gus}, {gl}, {gt} FROM grup WHERE id = {id}"
                query = query.format(**peremen)
                cursor.execute(query)
                for row in cursor:
                    get =   {
                    'title':     row['g_username'],
                    'last_news': row['g_last'],
                    'users':     row['g_users'].split(),
                    'nazv':      row['g_title']
                    }
                    # prow = Sqldb.och(prow)
                print('Я прошел')
                return get

    def get_us_param(id):
        with closing(connect()) as connection:
            with connection.cursor() as cursor:
                peremen = ['refers','balans']
                query = "SELECT {1},{2} FROM main WHERE uid = {3}"
                query = query.format(*peremen,id)
                cursor.execute(query)
                for row in cursor:
                    get = {
                    'refers': row['refers'],
                    'balans': row['balans']}
                return get

    def get_grup_param(id):
        per = False
        if (str(id).find("_p") > -1):
            id = re.sub("[_p]","",id)
            per = True

        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                znach = []
                peremen = ['g_username','g_id', 'g_title']
                for i in peremen:
                    query = "SELECT {0} FROM grup WHERE g_id = {1}"
                    query = query.format(i,id)
                    cursor.execute(query)
                    for row in cursor:
                        znach.append(row[i])

                get = {
                'title': znach[0],
                'g_id': znach[1],
                'nazv': znach[2]}
                if per:
                    get['g_id'] = str(get['g_id']) + "_p"
                # prow = Sqldb.och(prow)
                return get

    def r_users(user_f):
        znach = True
        id = user_f[0]
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = "SELECT uid FROM main ORDER BY uid"
                cursor.execute(query)
                for row in cursor:
                    if str(id) == str(row['uid']):
                        znach = False

            if znach:
                with conn.cursor() as cursor:
                    cursor = conn.cursor()
                    query = 'INSERT INTO main (uid, uname) VALUES ({0}, "{1}")'.format(
                    user_f[0], user_f[1])
                    cursor.execute(query)
                    conn.commit()
                    return False
            else:
                return True

    def p_chanel(id):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = 'SELECT utgrup, ungrup FROM main WHERE uid = {0}'
                query = guery.format(id)
                cursor.execute(query)
                for row in cursor:
                    mem = [row['utgrup'],row['ungrup']]
                    return mem

    def add_new_grup(grup):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                znach = True
                query = "SELECT g_id FROM grup WHERE g_id = {0}"
                query = query.format(grup['id'])
                for row in query:
                    if str(grup['id']) == str(row['g_id']):
                        znach = False

                if znach:
                    query = """
                                INSERT INTO grup
                                    (g_id, g_title, g_username, g_last, g_users)
                                VALUES
                                    ({id}, {title}, {username}, {last}, {u_id})
                            """
                    query = query.format(**grup)
                    cursor.execute(query)

                    if str(grup['id']) not in prow:
                        prow = Sqldb.ochstr(str(prow))
                        prow = (prow + " " + str(grup['id']))
                        if prow is None:
                            prow = grup['id']
                        # prow = prow + " " + grup["u_id"]
                        prow = Sqldb.ochstr(str(prow))
                        cursor.execute('UPDATE main SET ugroup = ? WHERE uid = ?',(prow,grup['u_id'],))
                        conn.commit()
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
                            if prow != []:
                                cursor.execute('UPDATE grup SET g_users = ? WHERE g_id = ?',(prow,grup['id'],))
                                conn.commit()
                            else:
                                cursor.execute('UPDATE grup SET g_users = ?, g_last = ? WHERE g_id = ?',(prow, grip['last'], grup['id'],))
                                conn.commit()
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
                                conn.commit()
                            return True
                        else:
                            cursor.close()
                            return False

    def edit_list(param):
        edit = {'func': param[0],
                'g_id': param[1],
                'uid':  param[len(param)-1]}
        if param[2] == "p":
            edit['pause'] = True
            edit['q_id_p'] = str(param[1])+'_p'
        else:
            edit['pause'] = False
        for_r = 3

        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                atr = {
                         'uid': edit['uid'],
                        'g_id': edit['g_id']
                        }

                query = "SELECT ugroup, utgrup FROM main WHERE uid = {uid}"
                query = query.format(**edit)
                cursor.execute(query)
                for row in cursor:
                    atr['ugroup'] = row['ugroup']
                    atr['utgrup'] = row['utgrup']

                query = "SELECT g_users FROM grup WHERE g_id = {g_id}"
                query = query.format(**edit)
                cursor.execute(query)

                for row in cursor:
                    atr['g_users'] = row['g_users']

                prow = atr['ugroup'].split()

                print(atr)

                if edit['g_id'] in prow or edit['g_id'] + '_p' in prow:

                    # Если удаление канала
                    if edit['func'] == "del":
                        # Если канал был на паузе удалить у юзера канал с приставкой "_p"
                        if edit['pause']:
                            prow.remove(str(edit['g_id'])+"_p")
                        else:
                            prow.remove(edit['g_id'])
                        # Уменьшаем текущее количество групп пользователя
                        atr['uqroup'] = obed(prow)
                        atr['utgrup'] -= 1
                        for_r = 0

                    # Если ставим канал на паузу
                    elif edit['func'] == "pau":
                        for i in range(len(prow)):
                            if prow[i] == edit['g_id']:
                                prow[i] += "_p"
                        atr['ugroup']  = obed(prow)
                        print(atr)
                        for_r = 1

                    elif edit['func'] == "beg":
                        for i in range(len(prow)):
                            if prow[i] == edit['g_id'] + "_p":
                                prow[i] = edit['g_id']
                            atr['ugroup']  = obed(prow)
                            for_r = [2, edit['g_id']]

                    prow = atr['g_users'].split()
                    # Если не запускаем канал, то удаляем юзера из списка подписчиков группы
                    if edit['func'] != "beg":
                        prow.remove(edit['uid'])
                        atr['g_users'] = obed(prow)
                    else:
                        prow.append(edit['uid'])
                        atr['g_users'] = obed(prow)


                    query = 'UPDATE main SET ugroup = "{ugroup}", utgrup = {utgrup} WHERE uid = {uid};'
                    query = query.format(**atr)
                    cursor.execute(query)

                    query = 'UPDATE grup SET g_users = "{g_users}" WHERE g_id = {g_id}'
                    query = query.format(**atr)
                    conn.commit()
                    cursor.execute(query)

        return for_r

    def add_ref(inviter):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = 'SELECT refers FROM main WHERE uid = {0}'.format(inviter)
                cursor.execute(query)
                inv = None
                for row in cursor:
                    inv = row['refers'] + 1

                query = 'UPDATE main SET refers = {0} WHERE uid = {1}'.format(inv,inviter)
                cursor.execute(query)
                conn.commit()

                if inv%2 == 0 and inv != 0:
                    guery = 'SELECT ungrup FROM main WHERE uid = ?'.format(inviter)
                    cursor.execute(query)
                    grup = None
                    for row in cursor:
                        grup = row['ungrup'] + 1
                    query = 'UPDATE main SET ungrup = ? WHERE uid = ?'.format(grup, inviter)
                    cursor.execute(query)
                    return True
                else:
                    return False

    def block(title):
        with closing(connect()) as connection:
            with connection.cursor() as cursor:
                query = "UPDATE grup SET g_role = -1 WHERE g_username = {0}"
                query = query.format(title)
                cursor.execute(query)
                conn.commit()


    def get_grup(id):
        with closing(connect()) as connection:
            with connection.cursor() as cursor:
                grup = None
                query = 'SELECT ugroup FROM main WHERE uid = {0}'.format(id)
                cursor.execute(query)
                for row in cursor:
                    grup = row['ugroup']
                return grup

    def get_user():
        with closing(connect()) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT uid FROM main WHERE uakt = 1")
                for row in cursor:
                    return row['uid']

    def grup_plus(id):
        with closing(connect()) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT utgrup FROM main WHERE uid = {0}".format(id))
                for row in cursor:
                    query = 'UPDATE main SET utgrup ={} WHERE uid = {}'.format(row['utgrup']+1,id)
                    cursor.execute(query)
                    conn.commit()
                return True

    def block_user(id):
        with closing(connect()) as connection:
            with connection.cursor() as cursor:
                query = 'UPDATE main SET uakt = -1 WHERE uid = {0}'.format(id)
                cursor.execute(query)
                conn.commit()



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
