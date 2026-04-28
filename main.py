from session import Session
from user import User

user    = User()
session = Session()

if __name__ == "__main__":

    # run once to create alice and bob, then comment out
    print(user.register("Alice", "Smith", "alice", "password123"))
    print(user.register("Bob",   "Jones", "bobj",   "password456"))

    # verify they were inserted
    user.cursor.execute("SELECT username, first, last FROM users")
    print(user.cursor.fetchall())