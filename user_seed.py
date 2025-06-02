from models import Peak, PeakList, db_session, User

test_user1 = User(username="ColinCool")
db_session.add(test_user1)
db_session.commit()
print("Added test user1")

test_user2 = User(username="LameJane")
db_session.add(test_user2)
db_session.commit()
print("Added test user2")
