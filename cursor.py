import sqlite3
from helpers import SingletonMeta, constant_time_compare

class Database(metaclass=SingletonMeta):
    connection =None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db.sqlite3")
            self.cursorobj = self.connection.cursor()
        return self.cursorobj

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection=None

    def is_table_available(self, table_name,keep_alive=False):
        c = self.connect()

        c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?",(table_name,))

        if c.fetchone()[0]==1:
            if not keep_alive:
                self.disconnect()
            return True

        if not keep_alive:
            self.disconnect()
        return False

    def initialize(self):
        import secrets
        master_key = secrets.token_urlsafe(32)
        c = self.connect()
        Database.create_table(c, 'auth')
        Database.create_table(c, 'users')
        Database.create_table(c,'submissions')

        c.execute("INSERT INTO auth VALUES(?)",(master_key,))
        self.connection.commit()
        self.disconnect()
        return master_key

    @staticmethod
    def create_table(c, table_name):
        if table_name == 'users':
            c.execute("CREATE TABLE IF NOT EXISTS users(username text, password text, client_id text, client_secret text)")
        elif table_name == 'submissions':
            c.execute("CREATE TABLE IF NOT EXISTS submissions(planned_unix_datetime integer, status text, username text, sub text, title text, text text, link text, image_name text, video text, flairid text, nsfw integer, submission_id text)")
        elif table_name == 'auth':
            c.execute("CREATE TABLE IF NOT EXISTS auth(master_key text)")
        else:
            pass

    def is_master_key_correct(self, input_key):
        c = self.connect()
        try:
            c.execute("SELECT master_key FROM auth ORDER BY rowid ASC LIMIT 1")
            master_key = c.fetchone()[0]
        except:
            master_key = None
            return False
        self.disconnect()
        return constant_time_compare(master_key, input_key)
