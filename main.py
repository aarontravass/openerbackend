from src.models.user import User
from src.models.user_relation import UserRelation
from src.models.test_plan_phases import TestPlanPhases
from src.models.test_plan import TestPlan
# u = User()
# u.print()
# #u.createOne({"first_name":"aaron","last_name":"t"})
# u.print()
rel = UserRelation()
rel.findShortestPath(2, 1)
# rel.createOne({"user_id":1, "manager_user_id":8})
#
phase = TestPlanPhases()
phase.prettyPrint()
#
# phase.approvePhase(
#     3, 4, 2, 2
# )

# test = TestPlan()
# test.print()
# test.createOne({
#     "plan_name":"production",
#     "user_id":1
# })