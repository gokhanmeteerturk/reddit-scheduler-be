# managers/users.py

from cursor import Database
from payloads import RedditUserPayload


class UserManager:
    def create_user(self, user: RedditUserPayload):
        db = Database()
        c = db.connect()
        c.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?)",
            (user.username, user.password, user.client_id, user.client_secret),
        )
        db.connection.commit()
        db.disconnect()
        return {"result": "Success"}

    def read_user(self, username: str):
        db = Database()
        c = db.connect()
        c.execute(
            "SELECT * FROM users WHERE username = ? ORDER BY rowid ASC LIMIT 1",
            (username,),
        )
        user_tuple = c.fetchone()
        db.disconnect()
        if user_tuple:
            return RedditUserPayload.from_tuple(user_tuple)
        else:
            return None

    def update_user(self, user: RedditUserPayload):
        db = Database()
        c = db.connect()
        c.execute(
            "UPDATE users SET password = ?, client_id = ?, client_secret = ? WHERE username = ?",
            (user.password, user.client_id, user.client_secret, user.username),
        )
        db.connection.commit()
        db.disconnect()
        return {"result": "Success"}

    def delete_user(self, username: str):
        db = Database()
        c = db.connect()
        c.execute(
            "DELETE FROM users WHERE username = ?",
            (username,),
        )
        db.connection.commit()
        db.disconnect()
        return {"result": "Success"}

    def list_users(self, page: int = 1, per_page: int = 10):
        db = Database()
        c = db.connect()
        offset = (page - 1) * per_page
        c.execute("SELECT * FROM users ORDER BY rowid ASC LIMIT ? OFFSET ?", (per_page, offset))
        user_tuples = c.fetchall()
        db.disconnect()

        users = []
        for user_tuple in user_tuples:
            user = RedditUserPayload.from_tuple(user_tuple)
            users.append(user)

        return users