from src.database.database import conn


class UserRelation:
    cursor = None

    def __init__(self):
        self.cursor = conn.cursor()
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
            print("user_id and manager_user_id is requried")
            return
        self.cursor.execute(
            """select * from public.users where id = %s or id = %s""",
            (data.get('user_id'), data.get('manager_user_id'))
        )
        row = self.cursor.fetchall()
        if (len(row) != 2):
            print("IDs are invalid")
            return
        self.cursor.execute(
            """INSERT INTO PUBLIC.user_relation VALUES(DEFAULT, %s, %s, DEFAULT, DEFAULT) RETURNING *""",
            (data.get('user_id'), data.get('manager_user_id'))
        )
        row = self.cursor.fetchone()
        conn.commit()
        if (row):
            print("Row inserted successfully")
            return
        print("Could not insert row")
        return

    def findShortestPath(self, user_id, manager_id):
        ceo_id = manager_id
        self.cursor.execute(
            """
            WITH RECURSIVE
            cte AS
            (
                SELECT p.manager_user_id,
                 concat(p.user_id, '->', p.manager_user_id) manager_path,
                 1 LENGTH
                FROM user_relation p
                WHERE p.user_id = %s

                UNION ALL

                SELECT p.manager_user_id,
                 concat(c.manager_path, '->', p.manager_user_id) manager_path,
                 c.length + 1 LENGTH
                FROM cte c
                INNER JOIN user_relation p ON p.user_id = c.manager_user_id
                WHERE c.manager_user_id <> %s
            )
            SELECT c.manager_path
            FROM cte c
            WHERE c.manager_user_id = %s
            ORDER BY c.length
            LIMIT 1;
            """,
            (user_id, ceo_id, ceo_id)
        )
        row = self.cursor.fetchone()
        if(row is None):
            print("No shortest path found. Check if  manager_id is manager of user_id")
            return
        print("Shortest path from %s to %s is %s"%(user_id, ceo_id, row[0]))
        return;

    def __del__(self):
        self.cursor.close()
