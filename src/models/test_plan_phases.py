from src.contants import TEST_PLAN_STATUS
from src.database.database import conn


class TestPlanPhases:
    cursor = None

    def __init__(self):
        self.cursor = conn.cursor()
        self.cursor.execute("select * from public.test_plan_phases")

    def print(self):
        self.cursor.execute("select * from public.test_plan_phases")
        print(self.cursor.fetchall())

    def execute(self, sql: str):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def addPhase(self, plan_id, user_id, risk):
        if TEST_PLAN_STATUS.get(risk) is None:
            print('Risk should be one of the follow: low, moderate, high')
            return
        if not plan_id or not user_id:
            print("Plan ID and User ID are required")
            return
        self.cursor.execute(
            """
            select * from public.test_plan
            where id=%s and user_id=%s and approved_on is null
            """,
            (plan_id, user_id)
        )
        rows = self.cursor.fetchall()
        if(len(rows) ==0):
            print("No plan found!")
            return
        self.cursor.execute(
            """
            INSERT INTO public.test_plan_phases VALUES(DEFAULT, %s, NULL, NULL, %s, DEFAULT, DEFAULT)
            """,
            (plan_id, risk)
        )
        conn.commit()
        print("Phase inserted!")
        return

    def approvePhase(self, manager_user_id, phase_id, plan_id, user_id):
        # find plan and determine status
        # if plan status is high, then find indirect managers
        # else find direct managers
        self.cursor.execute(
            """select * from users where id in (%s, %s)""",
            (user_id, manager_user_id)
        )
        row = self.cursor.fetchall()
        if (len(row) != 2):
            print("User ID and Manager ID are invalid")
            return
        self.cursor.execute(
            """select risk, user_id, public.test_plan_phases.approved_on 
            from public.test_plan inner join public.test_plan_phases
            on public.test_plan.id=public.test_plan_phases.test_plan_id
            where user_id=%s and test_plan.id=%s and
            test_plan_phases.id=%s
            """,
            (user_id, plan_id, phase_id)
        )
        row = self.cursor.fetchall()
        print(row)
        if (len(row) != 1):
            print("Plan or Phase ID are invalid")
            return
        if (row[0][2]):
            print("Phase has already been approved")
            return
        all_managers = self.__findAllManagersByUserID(user_id)

        if (row[0][0] == TEST_PLAN_STATUS.get("low")):
            if (manager_user_id in all_managers or manager_user_id == user_id):
                self.cursor.execute(
                    """
                    update test_plan_phases 
                    set approved_on=CURRENT_TIMESTAMP,
                    manager_user_id=%s,
                    updated_at=CURRENT_TIMESTAMP
                    where id=%s
                    """,
                    (manager_user_id, phase_id)
                )
                conn.commit()
                print("Approved successfully!")
                return
            else:
                print("Unauthorized")
                return
        elif (row[0][0] == TEST_PLAN_STATUS.get("moderate")):
            if (manager_user_id in self.__findDirectManagers(user_id)):
                self.cursor.execute(
                    """
                    update test_plan_phases 
                    set approved_on=CURRENT_TIMESTAMP,
                    manager_user_id=%s,
                    updated_at=CURRENT_TIMESTAMP
                    where id=%s
                    """,
                    (manager_user_id, phase_id)
                )
                conn.commit()
                print("Approved successfully!")
                return
            else:
                print("Unauthorized")
                return
        else:
            if (manager_user_id in all_managers):
                self.cursor.execute(
                    """
                    update test_plan_phases 
                    set approved_on=CURRENT_TIMESTAMP,
                    manager_user_id=%s,
                    updated_at=CURRENT_TIMESTAMP
                    where id=%s
                    """,
                    (manager_user_id, phase_id)
                )
                conn.commit()
                print("Approved successfully!")
                return
            else:
                print("Unauthorized")
                return

    def __findAllManagersByUserID(self, user_id):
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
            GROUP BY c.manager_user_id
            """,
            (user_id,)
        )
        rows = self.cursor.fetchall()
        manager_list = []
        for r in rows:
            print(r)
            manager_list.append(r[0])
        return manager_list

    def __findAllManagers(self):
        return self.execute(
            """
            WITH RECURSIVE cte AS
            (
                SELECT p.manager_user_id, p.user_id
                FROM user_relation p UNION ALL
                SELECT p.manager_user_id, c.user_id
                FROM cte c
                INNER JOIN user_relation p ON p.user_id = c.manager_user_id
            )
            SELECT *
            FROM cte AS C
            GROUP BY C.manager_user_id, C.user_id
            """)

    def __findDirectManagers(self, user_id):
        self.cursor.execute(
            """
           SELECT manager_user_id FROM user_relation WHERE user_id=%s
            """,
            (user_id,)
        )

        direct_manager_list = []
        for r in self.cursor.fetchall():
            direct_manager_list.append(r[0])
        return direct_manager_list

    def prettyPrint(self):
        plans = self.execute(
            """	
            SELECT 
            plan_name, 
            risk, 
            test_plan_phases.created_at, 
            test_plan_phases.approved_on, 
            concat(first_name, ' ' , last_name) AS name,
            user_id
            FROM test_plan
            LEFT JOIN test_plan_phases ON test_plan.id=test_plan_phases.test_plan_id
            LEFT JOIN users ON test_plan_phases.manager_user_id=users.id
	        """
        )
        users = self.execute(
            "select id, concat(first_name, ' ', last_name) as name from public.users"
        )
        user_dict = {}
        for u in users:
            user_dict[u[0]] = u[1]
        manager_dict = {}
        all_managers = self.__findAllManagers()
        for manager_rel in all_managers:
            if (manager_dict.get(manager_rel[1]) is None):
                manager_dict[manager_rel[1]] = [manager_rel[0]]
            else:
                manager_dict[manager_rel[1]].append(manager_rel[0])
        plan_list = {}
        for plan in plans:
            if plan_list.get(plan[0]) is None:
                plan_list[plan[0]] = []
            if(plan[1] is None):
                plan_list[plan[0]]=[
                    {
                        "message": "No phases have been added!"
                    }
                ]
            else:
                plan_list[plan[0]].append(
                    {
                        "message":None,
                        "risk": plan[1],
                        "created_at": plan[2].strftime("%m/%d/%Y, %H:%M:%S"),
                        "approved_on": plan[3].strftime("%m/%d/%Y, %H:%M:%S") if plan[3] is not None else None,
                        "approved_by": plan[4] if plan[4] != ' ' else None,
                        "managers": [ user_dict.get(man) for man in manager_dict[plan[5]]],
                        "created_by_user_id": plan[5]
                    }
                )
        for key in plan_list.keys():
            print("Plan: ", key)
            print('--------------------------------------')
            for val in plan_list[key]:
                if val['message'] is None:
                    print("Phase:")
                    print("Risk: ", val['risk'])
                    print("Created At: ", val['created_at'])
                    if val['approved_on']:
                        print("Approved on: ", val['approved_on'])
                        print("Approved By: ", val['approved_by'])
                    else:
                        if(val['risk']=='low'):
                            val['managers'].append(user_dict.get(val['created_by_user_id']))
                        print("Managers that can approve: ", ', '.join(val['managers']))
                else:
                    print(val['message'])
                print('--------------------------------------')
            print('')



    def __del__(self):
        self.cursor.close()





















