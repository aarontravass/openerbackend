import psycopg2

from src.database.database import conn
class TestPlanPhases:
    records:list
    cursor:psycopg2.cursor

    def __init__(self):
        self.cursor = conn().cursor()
        self.cursor.execute("select * from public.test_plan")
        self.records=self.cursor.fetchall()

    @classmethod
    def print(self):
        print(self.records)

    @classmethod
    def execute(self, sql: str):
        self.cursor.execute(sql)
        return self.cursor.fetchall()


    def __del__(self):
        self.cursor.close()