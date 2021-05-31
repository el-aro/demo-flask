


class NoData(Exception):
    pass


class MoreThatOne(Exception):
    pass


class DataAccessObject:
    '''control the mysqlconnection
    read ans save data'''

    def __init__(self, db):
        self.db = db

    def get_anything(self, sql):
        with self.db.connect() as conn:
            resultproxy = conn.execute(sql)
            row = [dict(rowproxy.items()) for rowproxy in resultproxy]
        if len(row) == 1:
            return row[0]
        if len(row):
            return row
        return None

    def save_anything(self, sql, data = None):
        with self.db.connect() as conn:
            if data:
                result = conn.execute(sql, data)
            else:
                result = conn.execute(sql)
        return result.lastrowid

    def delete_person_by_id(self, id):
        sql = f'''
            delete from Persons where id = {id}
        '''
        return self.save_anything(sql)

    def get_persons(self, offset, perpage):
        sql = f'''
            select *  from Persons limit {perpage} offset {offset}
        '''
        return self.get_anything(sql)

    def get_persons_total(self):
        sql = '''
            select count(*) as total from Persons
        '''
        return self.get_anything(sql)

    def update_person(self, data):
        sql = '''
        update Persons set `last_name` =  %(last_name)s ,
        `first_name` = %(first_name)s,
        `date_of_birth` = %(date_of_birth)s ,
        `email` = %(email)s  where id = %(id)s
        '''
        return self.save_anything(sql,data)

    def get_person_by_email(self, email):
        sql = f'''
            select  * from Persons where email = "{email}"
        '''
        return self.get_anything(sql)

    def get_person_by_id(self, id):
        sql = f'''
            select  * from Persons where id = {id}
        '''
        return self.get_anything(sql)

    def save_person(self, data):
        sql = '''
            INSERT INTO Persons (
                `last_name`,
                `first_name`,
                `date_of_birth`,
                `email`
            )
            VALUES (
            %(last_name)s,
            %(first_name)s,
            %(date_of_birth)s,
            %(email)s
            )
        '''
        return self.save_anything(sql, data)