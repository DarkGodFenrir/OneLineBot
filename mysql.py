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
                                g.self_id 
                            FROM 
                                user_group AS ug
                            LEFT JOIN 
                                `groups` AS g 
                            ON 
                                ug.group_id  = g.group_id 
                            LEFT JOIN 
                                users AS u 
                            ON 
                                ug.telegram_id = u.telegram_id 
                            WHERE 
                                u.status = 1 
                                    AND 
                                ug.paused = 0 
                                    AND 
                                g.status = 0
                            GROUP  BY g.group_id 
                                """)
            for row in cursor:
                prow.append(row['self_id'])
            return prow


def get_number():
    with closing(connect()) as conn:
        with conn.cursor() as cursor:
            query = '''
            SELECT
                news_number
            FROM
                memory
                    '''
            cursor.execute(query)
            for row in cursor:
                return row['news_number']


def edit_memory_number(self):
    with closing(connect()) as conn:
        with conn.cursor() as cursor:
            query = f'''
                    UPDATE
                        memory
                    SET
                        news_number = {self} 
                    '''
            cursor.execute(query)
            conn.commit()


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

    def get_users(self):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = f'''
                        SELECT 
                            ug.telegram_id 
                        FROM 
                            user_group AS ug
                        LEFT JOIN users AS u
                        ON ug.telegram_id = u.telegram_id 
                        WHERE 
                            ug.group_id = {self} AND 
                            ug.paused = 0 AND 
                            u.status != -1
                        '''
                cursor.execute(query)
                mem = []
                for row in cursor:
                    mem.append(row['telegram_id'])
            return mem

    def get_param(self):
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = f'''SELECT 
                                tag,
                                group_id,  
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
        print(self)
        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = f'''
                        SELECT 
                            *
                        FROM
                            groups
                        WHERE
                            group_id = {self['group_id']}
                        '''
                cursor.execute(query)

                mem = []
                for row in cursor:
                    mem.append(row)

                print(mem)
                if mem:
                    query = f'''
                            SELECT
                                paused
                            FROM
                                user_group 
                            WHERE
                                group_id = {self['group_id']}
                                    AND
                                telegram_id = {self['telegram_id']}
                            '''
                    cursor.execute(query)

                    mem = []
                    for row in cursor:
                        mem.append(row)

                    if not mem:
                        query = f'''
                                INSERT INTO
                                    user_group (telegram_id, group_id)
                                VALUES
                                    ({self['telegram_id']}, {self['group_id']}
                                '''
                        cursor.execute(query)
                        conn.commit()
                        return True
                    else:
                        return False

                else:
                    query = f'''
                                INSERT INTO
                                    user_group (telegram_id, group_id)
                                VALUES
                                    ({self['telegram_id']}, {self['group_id']})
                            '''
                    cursor.execute(query)

                    query = f'''
                                INSERT INTO
                                    groups (group_id, tag, name, last_number)
                                VALUES
                                    ({self['group_id']},'{self['tag']}', '{self['name']}', {self['last_number']})
                            '''

                    cursor.execute(query)
                    conn.commit()
                    return True


    def edit_list(self):

        print(self)
        edit = {'func': self[0],
                'group_id': int(self[1]),
                'telegram_id': int(self[2])
                }
        for_r = 3

        with closing(connect()) as conn:
            with conn.cursor() as cursor:
                query = None

                if edit['func'] == 'pau':
                    query = f'''
                            UPDATE 
                                user_group
                            SET
                               paused = 1
                            WHERE 
                                group_id = {edit['group_id']} AND
                                telegram_id = {edit['telegram_id']}
                            '''
                    for_r = 1

                elif edit['func'] == 'beg':
                    for_r = {'num': 2, 'flag': False}

                    query = f'''
                            SELECT
                                g.tag, g.last_number, ug.paused
                            FROM 
                                user_group AS ug
                            LEFT JOIN
                                groups AS g
                            ON
                                ug.group_id = g.group_id
                            WHERE
                                ug.group_id = {edit['group_id']}
                            '''
                    cursor.execute(query)

                    mem = []
                    for row in cursor:
                        edit['last_number'] = row['last_number']
                        edit['tag'] = row['tag']
                        if row['paused'] == 0:
                            mem.append(row)

                    if not mem:
                        for_r['flag'] = True
                        for_r['tag'] = edit['tag']
                        for_r['last_number'] = edit['last_number']

                    query = f'''
                            UPDATE
                                user_group
                            SET
                                paused = 0
                            WHERE 
                                group_id = {edit['group_id']} AND
                                telegram_id = {edit['telegram_id']}
                            '''

                elif edit['func'] == 'del':
                    query = f'''
                            DELETE FROM 
                                user_group
                            WHERE 
                                group_id = {edit['group_id']} AND
                                telegram_id = {edit['telegram_id']}
                            '''
                    cursor.execute(query)

                    query = f'''
                            SELECT 
                                subscriptions
                            FROM
                                users
                            WHERE
                                telegram_id = {edit['telegram_id']}
                            '''
                    cursor.execute(query)

                    mem = None
                    for row in cursor:
                        mem = row['subscriptions']

                    query = f'''
                            UPDATE
                                users
                            SET
                                subscriptions = {mem - 1}
                            WHERE
                                telegram_id = {edit['telegram_id']}
                            '''
                    for_r = 0

                cursor.execute(query)
                conn.commit()
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
                                g.name, g.tag, 
                                ug.paused, ug.group_id
                            FROM 
                                user_group AS ug
                            LEFT JOIN
                                groups AS g
                            ON
                                ug.group_id = g.group_id
                            WHERE 
                                ug.telegram_id = {self}
                            '''
                cursor.execute(query)
                memory = []
                for row in cursor:
                    memory.append(row)
                return memory

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
                                    subscriptions ={row["subscriptions"] + 1} 
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
