from src.database.database import conn


class UserRelation:
    cursor = None

    def __init__(self):
        self.cursor = conn().cursor()
        self.cursor.execute("select * from public.user_relation")
        self.records = self.cursor.fetchall()

    def print(self):
        self.cursor.execute("select * from public.user_relation")
        print(self.cursor.fetchall())

    def execute(self, sql: str):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def createOne(self, data):
        if not data.get('user_id') or not data.get('manager_user_id'):
            print("First Name and Last Name is requried")
            return
        self.cursor.execute(
            """select * from public.users where id = %s or id = %s""",
            (data.get('user_id'), data.get('manager_user_id'))
        )
        row = self.cursor.fetchall()
        print(row)
        if (len(row) != 2):
            print("IDs are invalid")
            return
        self.cursor.execute(
            """INSERT INTO PUBLIC.user_relation VALUES(DEFAULT, %s, %s, DEFAULT, DEFAULT);""",
            (data.get('user_id'), data.get('manager_user_id'))
        )
        row = self.cursor.fetchone()
        conn.commit()
        if (row):
            print("Row inserted successfully")
            return
        print("Could not insert row")
        return

    def __del__(self):
        self.cursor.close()
