import mysql.connector as dbconnect
import sys
from .user import User

class DbConnection:

    def __init__(self):
        self.users = {}
        pass

    def connect(self):
        self.connexion = dbconnect.connect(user='root', database='mangadb', password='toto', host='127.0.0.1')

    #def createTable(self):
        #USE mangadb;
        #CREATE TABLE users
        #(
        #    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
        #    login VARCHAR(100) NOT NULL,
        #    psswd VARCHAR(100) NOT NULL,
        #    UNIQUE(login),
        #    PRIMARY KEY(id)
        #)
        #ENGINE=INNODB;


    def disconnect(self):
        self.connexion.close()

    def _checkUser(self, user):
        if user is None:
            return False
        if not isinstance(user, User):
            return False
        return True

    def saveUser(self, user):
        if not self._checkUser(user):
            return
        name = user.id
        password_hash = user.password_hash
        #first check if exists...
        cursor = self.connexion.cursor()
        query = "SELECT COUNT(1) FROM users WHERE login = \'{}\'".format(name)
        cursor.execute(query)
        if cursor.fetchone()[0]:
            self._log("user {} found, update it".format(name))
            #entry exists, update it
            query = "UPDATE users SET psswd=\'{}\' WHERE login=\'{}\'".format(password_hash, name)
            cursor.execute(query)
        else:
            self._log("user {} not found, create it".format(name))
            #no entry, create it
            query = "INSERT INTO users (login, psswd) VALUES (%s, %s)"  #.format(name, password_hash)
            cursor.execute(query, (name, password_hash))
        self.connexion.commit()
        cursor.close()

    def delUser(self, user):
        if not self._checkUser(user):
            return
        name = user.name
        cursor = self.connexion.cursor()
        query = "SELECT COUNT(1) FROM users WHERE login = \'{}\'".format(name)
        cursor.execute(query)
        if cursor.fetchone()[0]:
            self._log("user {} found, delete it".format(name))
            #entry exists, update it
            query = "DELETE FROM users WHERE login=\'{}\'".format(name)
            cursor.execute(query)
            self.connexion.commit()
            #clean cache
            if user.id in self.users:
                del self.users[user.id]
        cursor.close()

    def getUser(self, login):
        user = None
        if login is None:
            return None
        if login in self.users:
            user = self.users[login]
            self._log("db: load user from cache -> user is {}".format(user))
        else:
            cursor = self.connexion.cursor()
            query = "SELECT login, psswd FROM users WHERE login = \'{}\'".format(login)
            cursor.execute(query)
            for (login, psswd) in cursor:
                user = User(login, psswd)
                #store it in cache
                self.users[user.id] = user
            cursor.close()
            self._log("db: load user from base -> user is {}".format(user))
        return user

    def _log(self, message):
        sys.stdout.write(message)
        sys.stdout.write('\n')
        sys.stdout.flush()
