

from src.database.database import conn

class User:
    cursor=None;
   

    def __init__(self):
        self.cursor = conn.cursor()
        self.cursor.execute("select * from public.users")



    def print(self):
        self.cursor.execute("select * from public.users")
        print(self.cursor.fetchall())


    def execute(self, sql: str):
        self.cursor.execute(sql)
        return self.cursor.fetchall()


    def createOne(self, data):
        if(not data.get('first_name') or not data.get('last_name')):
            print( "First Name and Last Name is requried")
            return
        self.cursor.execute(
            """INSERT INTO PUBLIC.users VALUES(DEFAULT, %s, %s, DEFAULT, DEFAULT) RETURNING *""",
            (data.get('first_name'), data.get('last_name'))
        )
        row = self.cursor.fetchone()
        conn.commit()
        print(row)
        if(row):
            print("Row inserted successfully")
            return
        print("Could not insert row")
        return

    def __del__(self):
        self.cursor.close()