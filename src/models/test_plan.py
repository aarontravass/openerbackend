import psycopg2

from src.database.database import conn
class TestPlanPhases:
    cursor:psycopg2.cursor

    def __init__(self):
        self.cursor = conn().cursor()
        self.cursor.execute("select * from public.test_plan")
        self.records=self.cursor.fetchall()


    def print(self):
        self.cursor.execute("select * from public.test_plan")
        print(self.cursor.fetchall())


    def execute(self, sql: str):
        self.cursor.execute(sql)
        return self.cursor.fetchall()


    def createOne(self, data):
        if(not data.get('user_id') or not data.get('plan_name')):
            print( "User ID and Plan Name is requried")
            return
        self.cursor.execute(
            """select * from public.users where id = %s""",
            (data.get('user_id'))
        )
        row = self.cursor.fetchone()

        print(row)
        if(not row):
            print("No such user exists")
            return
        self.cursor.execute(
            """INSERT INTO public.test_plan VALUES (DEFAULT, %s, '%s', NULL, DEFAULT, DEFAULT);""",
            (data.get('user_id'), data.get('plan_name'))
        )
        row = self.cursor.fetchone()
        conn.commit()
        if(row):
            print("New test plan added!")
            return
        print("Could not insert row")
        return


    def __del__(self):
        self.cursor.close()