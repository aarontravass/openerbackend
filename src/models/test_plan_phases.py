from src.contants import TEST_PLAN_STATUS
from src.database.database import conn
class TestPlanPhases:
    cursor=None

    def __init__(self):
        self.cursor = conn.cursor()
        self.cursor.execute("select * from public.test_plan_phases")
        self.records=self.cursor.fetchall()

    def print(self):
        self.cursor.execute("select * from public.test_plan_phases")
        print(self.cursor.fetchall())


    def execute(self, sql: str):
        self.cursor.execute(sql)
        return self.cursor.fetchall()


    def approvePhase(self, manager_user_id, phase_id, plan_id, user_id):
        #find plan and determine status
        #if plan status is high, then find indirect managers
        # else find direct managers
        self.cursor.execute(
            """select * from users where id in (%s, %s)""",
            (user_id, manager_user_id)
        )
        row = self.cursor.fetchall()
        if(len(row)!=2):
            print("User ID and Manager ID are invalid")
            return
        self.cursor.execute(
            """select risk, user_id, public.test_plan_phases.approved_on 
            from public.test_plan inner join public.test_plan_phases
            on public.test_plan.id=public.test_plan_phases.test_plan_id
            where user_id=%s and test_plan.id=%s 
            test_plan_phases.id=%s
            """,
            (user_id, plan_id, phase_id)
        )
        row=self.cursor.fetchall()
        print(row)
        if(len(row)!=1):
            print("Plan or Phase ID are invalid")
            return
        if(row[0][2]):
            print("Phase has already been approved")
            return
        if(row[0][0]==TEST_PLAN_STATUS.get("low")):

        elif(row[0][0]==TEST_PLAN_STATUS.get("moderate")):

        else:

    def __findIndirectManagers(self, user_id):
        self.cursor.execute(
            """
            WITH RECURSIVE
            cte AS
            (
            	SELECT p.manager_user_id
            	FROM user_relation p
            	WHERE p.user_id = %s

            	UNION ALL

            	SELECT p.manager_user_id
            	FROM cte c
            	INNER JOIN user_relation p ON p.user_id = c.manager_user_id
            )
            SELECT *
            FROM cte AS C
            WHERE c.manager_user_id NOT IN (SELECT manager_user_id FROM user_relation WHERE user_id=%s)
            GROUP BY c.manager_user_id
            """,
            (user_id, user_id)
        )

        manager_list = []
        for r in self.cursor.fetchall():
            manager_list.append(r[0])
        return manager_list

    def __findDirectManagers(self, user_id):
        self.cursor.execute(
            """
           SELECT manager_user_id FROM user_relation WHERE user_id=%s
            """,
            (user_id)
        )

        direct_manager_list = []
        for r in self.cursor.fetchall():
            direct_manager_list.append(r[0])
        return direct_manager_list




    def __del__(self):
        self.cursor.close()


