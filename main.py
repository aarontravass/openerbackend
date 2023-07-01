from src.models.user import User
from src.models.user_relation import UserRelation
#
# u = User()
# u.print()
# #u.createOne({"first_name":"aaron","last_name":"t"})
# u.print()
rel = UserRelation()
rel.findShortestPath()