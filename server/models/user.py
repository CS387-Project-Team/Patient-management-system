from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password
        self.authenticated = False
    
    def get(self, id, conn):
        cursor = conn.cursor()
        sql = "select * from login where id = {}".format(id)
        cursor.execute(sql)
        lu = cursor.fetchone()
        if lu is not None:
            self.id = lu[0]
            self.email = lu[1]
            self.password = lu[2]
            return self
        else:
            return None