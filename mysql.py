from contextlib import closing
import pymysql
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
    to_string = ""
    for m in mem:
        to_string += m + " "
    return to_string


def get_max_group():
    prow = []
    with closing(connect()) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                                SELECT
                                    self_id
                                FROM
                                    groups
                                WHERE
                                    status != -1
                                AND
                                    users != ''
                                """)
            for row in cursor:
                prow.append(row['self_id'])
            return prow


class Sqldb:

    def edit_number(self, param):
        print(self, param)
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = f'''UPDATE 
                                groups 
                            SET 
                                last_number = ({self}) 
                            WHERE 
                                tag = "{param["tag"]}"'''
                cursor.execute(query)
                conn.commit()

    def get_param(self):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = f'''SELECT 
                                tag, 
                                users, 
                                last_number, 
                                name 
                            FROM 
                                groups 
                            WHERE 
                                self_id = {self}
                        '''
                cursor.execute(query)
                for row in cursor:
                    return row

    def get_us_param(self):
        with closing(connect()) as connection:
            with connection.cursor() as cursor:
                query = f"SELECT refers, balance FROM users WHERE telegram_id = {self}"
                cursor.execute(query)
                for row in cursor:
                    return row

    def get_group_param(self):
        per = False
        if str(self).find("_p") > -1:
            group_id = self[:-2]
            per = True
        else:
            group_id = self

        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = f'''SELECT
                                name, tag, group_id 
                            FROM 
                                groups 
                            WHERE 
                                group_id = {group_id}
                        '''
                cursor.execute(query)

                get = None
                for row in cursor:
                    get = row

                if per:
                    get['group_id'] = str(get['group_id']) + "_p"
                return get

    def login_user(self):
        value = True
        telegram_id = self[0]
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = "SELECT telegram_id FROM users ORDER BY telegram_id"
                cursor.execute(query)
                for row in cursor:
                    if str(telegram_id) == str(row['telegram_id']):
                        value = False

                if value:
                    query = f'''INSERT INTO 
                                    users (telegram_id, name) 
                                VALUES 
                                    ({self[0]}, "{self[1]}")'''
                    cursor.execute(query)
                    conn.commit()
                    return False

                else:
                    conn.commit()
                    return True

    def channel_check(self):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = f'''SELECT 
                                subscriptions, max_groups 
                            FROM 
                                users 
                            WHERE 
                                telegram_id = {self}'''

                cursor.execute(query)
                for row in cursor:
                    mem = [row['subscriptions'], row['max_groups']]
                    return mem

    def add_new_group(self):
        with closing(connect()) as conn:
            print(self)
            with conn.cursor() as cursor:
                value = True
                query = f"SELECT group_id FROM groups WHERE group_id = {self['group_id']}"
                cursor.execute(query)
                for row in cursor:
                    if str(self['group_id']) == str(row['group_id']):
                        value = False

                if value:
                    query = f"""
                                INSERT INTO groups
                                    (group_id, , tag, last_news, users)
                                VALUES
                                    ({self['group_id']}, {self['tag']}, {self['name']},
                                    {self['last_numbers']}, {self['telegram_id']})
                            """
                    cursor.execute(query)

                    query = f"SELECT groups FROM users WHERE telegram_id = {self['telegram_id']}"
                    cursor.execute(query)
                    prow = None
                    for row in cursor:
                        prow = row['groups'].split()

                    if str(self['id']) not in prow:
                        prow = (prow + " " + str(self['id']))
                        if prow is None:
                            prow = self['id']

                        query = f'''UPDATE
                                        users
                                    SET 
                                        groups = {prow} 
                                    WHERE 
                                        telegram_id = {self["telegram_id"]}
                                '''
                        cursor.execute(query)
                    conn.commit()
                    return True

                else:
                    with conn:
                        query = f"SELECT users FROM groups WHERE group_id = {self['group_id']}"
                        cursor.execute(query)
                        check = None
                        for row in cursor:
                            check = row['users'].split()

                        if str(self['telegram_id']) not in check:

                            check = (obed(check) + " " + str(self['telegram_id']))
                            query = f'''UPDATE 
                                            groups 
                                        SET 
                                            users = {check}, 
                                            g_last = {self['last_numbers']} 
                                        WHERE 
                                            group_id = {self['group_id']}
                                    '''
                            cursor.execute(query)

                            query = f'''SELECT
                                            groups 
                                        FROM 
                                            users 
                                        WHERE 
                                            telegram_id = {self["telegram_id"]}
                                    '''
                            cursor.execute(query)
                            check = None
                            for row in cursor:
                                check = row['groups'].split()

                            if str(self['group_id']) not in check or str(self['group_id'])+'_p' not in check:

                                check = (obed(check) + " " + str(self['group_id']))
                                print(self)

                                query = f'''
                                            UPDATE 
                                                users 
                                            SET 
                                                groups = {check} 
                                            WHERE 
                                                telegram_id = {self['telegram_id']}
                                        '''
                                cursor.execute(query)
                                conn.commit()
                            return True
                        else:
                            return False

    def edit_list(self):

        print(self)
        edit = {'func': self[0],
                'group_id': self[1],
                'telegram_id': int(self[-1])
                }
        if self[2] == "p":
            edit['pause'] = True
            edit['group_id_p'] = str(self[1]) + '_p'
        else:
            edit['pause'] = False
        for_r = 3

        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                atr = {
                    'telegram_id': edit['telegram_id'],
                    'group_id': edit['group_id']
                }

                query = f'''SELECT 
                                groups, subscriptions
                            FROM 
                                users 
                            WHERE 
                                telegram_id = {edit['telegram_id']}
                        '''
                cursor.execute(query)

                for row in cursor:
                    atr['groups'] = row['groups']
                    atr['subscriptions'] = row['subscriptions']

                query = f"SELECT users, tag FROM groups WHERE group_id = {edit['group_id']}"
                cursor.execute(query)

                for row in cursor:
                    atr['users'] = row['users']
                    atr['tag'] = row['tag']

                prow = atr['groups'].split()

                if edit['group_id'] in prow or edit['group_id'] + '_p' in prow:

                    # Если удаление канала
                    if edit['func'] == "del":
                        # Если канал был на паузе удалить у юзера канал с приставкой "_p"
                        if edit['pause']:
                            prow.remove(str(edit['group_id']) + "_p")
                        else:
                            prow.remove(edit['group_id'])
                        # Уменьшаем текущее количество групп пользователя
                        atr['groups'] = obed(prow)
                        atr['subscriptions'] -= 1
                        for_r = 0

                    # Если ставим канал на паузу
                    elif edit['func'] == "pau":
                        for i in range(len(prow)):
                            if prow[i] == edit['group_id']:
                                prow[i] += "_p"
                        atr['groups'] = obed(prow)
                        print(atr)
                        for_r = 1

                    elif edit['func'] == "beg":
                        check = prow
                        for i in range(len(prow)):
                            if prow[i] == edit['group_id'] + "_p":
                                prow[i] = edit['group_id']
                            atr['groups'] = obed(prow)
                            for_r = {"num": 2, "tag": atr['tag']}
                            if check:
                                for_r["flag"] = True
                            else:
                                for_r["flag"] = False

                    prow = atr['users'].split()
                    # Если не запускаем канал, то удаляем юзера из списка подписчиков группы
                    if edit['func'] != "beg":
                        if str(edit['telegram_id']) in prow:
                            prow.remove(str(edit['telegram_id']))
                        atr['users'] = obed(prow)
                    else:
                        prow.append(str(edit['telegram_id']))
                        atr['users'] = obed(prow)

                    query = f'''UPDATE 
                                    users 
                                SET 
                                    groups = "{atr['groups']}", 
                                    subscriptions = {atr['subscriptions']} 
                                WHERE 
                                    telegram_id = {atr['telegram_id']};'''

                    cursor.execute(query)

                    query = f'''UPDATE 
                                    groups 
                                SET 
                                    users = "{atr["users"]}" 
                                WHERE 
                                    group_id = {atr["group_id"]}
                                '''
                    conn.commit()
                    cursor.execute(query)

        return for_r

    def add_ref(self):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = f'SELECT refers FROM users WHERE telegram_id = {self}'
                cursor.execute(query)
                inv = None
                for row in cursor:
                    inv = row['refers'] + 1

                query = f'UPDATE users SET refers = {inv} WHERE telegram_id = {self};'
                cursor.execute(query)

                if inv % 2 == 0 and inv != 0:
                    query = f'SELECT max_groups FROM users WHERE telegram_id = {self}'
                    cursor.execute(query)
                    group = None
                    for row in cursor:
                        group = row['max_groups'] + 1
                    query = f'UPDATE users SET max_groups = {group} WHERE telegram_id = {self}'
                    cursor.execute(query)
                    conn.commit()
                    return True
                else:
                    return False

    def block(self):
        with closing(connect()) as conn:
            print(self)
            with conn.cursor() as cursor:
                query = f"UPDATE groups SET status = -1 WHERE tag = '{self}'"
                cursor.execute(query)
                conn.commit()

    def get_group(self):
        with closing(connect()) as connection:
            with connection.cursor() as cursor:
                query = f'''SELECT
                                groups 
                            FROM 
                                users 
                            WHERE 
                                telegram_id = {self}
                            '''
                cursor.execute(query)
                for row in cursor:
                    return row['groups']

    @staticmethod
    def get_user():
        with closing(connect()) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT telegram_id FROM users WHERE status = 1")
                for row in cursor:
                    return row['telegram_id']

    def group_plus(self):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = f'SELECT subscriptions FROM users WHERE telegram_id = {self}'
                cursor.execute(query.format(self))
                for row in cursor:
                    query = f'''UPDATE
                                    users 
                                SET 
                                    subscriptions ={row["subscriptions"]+1} 
                                WHERE 
                                    telegram_id = {self}
                            '''
                    cursor.execute(query)
                    conn.commit()
                return True

    def block_user(self):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = f'UPDATE users SET status = -1 WHERE telegram_id = {self}'
                cursor.execute(query)
                conn.commit()
