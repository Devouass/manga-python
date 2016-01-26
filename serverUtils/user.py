from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.hash import sha256_crypt


class User:

    SECRET_KEY = "aSecretKey"

    def __init__(self, login, password_hash = None):
        self.id = login
        self.password_hash = password_hash
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

    def generate_auth_token(self, expiration = 600):
        s = Serializer(User.SECRET_KEY, expires_in = expiration)
        return s.dumps({ 'id': self.id })

    def __str__(self):
        return "name: {}".format(self.id)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(User.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        #user = User.query.get(data['id'])
        return data['id']#user
