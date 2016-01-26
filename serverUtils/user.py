from passlib.hash import sha256_crypt


class User:

    SECRET_KEY = "aSecretKey"
    user = None

    def __init__(self, login, password_hash = None):
        self.id = login
        self.password_hash = password_hash
        self.authenticated = False
        pass

    def hash_password(self, password):
        self.password_hash = sha256_crypt.encrypt(password)

    def verify_password(self, password):
        res = False
        try:
            res = sha256_crypt.verify(password, self.password_hash)
        except ValueError:
            #TODO log...
            pass
        return res

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __str__(self):
        return "name: {}, authenticated: {}".format(self.id, self.authenticated)

    @staticmethod
    def get(user_id):
        return User.user
