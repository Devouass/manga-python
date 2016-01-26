import mysql.connector as dbconnect
import sys
from .user import User

class DbConnection:

    def __init__(self):
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

    def saveUser(self, name, password_hash):
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

    def delUser(self, name):
        cursor = self.connexion.cursor()
        query = "SELECT COUNT(1) FROM users WHERE login = \'{}\'".format(name)
        cursor.execute(query)
        if cursor.fetchone()[0]:
            self._log("user {} found, delete it".format(name))
            #entry exists, update it
            query = "DELETE FROM users WHERE login=\'{}\'".format(name)
            cursor.execute(query)
            self.connexion.commit()
        cursor.close()

    def getUser(self, login):
        self._log("login is {}".format(login))
        user = None
        cursor = self.connexion.cursor()
        query = "SELECT login, psswd FROM users WHERE login = \'{}\'".format(login)
        cursor.execute(query)
        for (login, psswd) in cursor:
            self._log("login: {}, pssw: {}".format(login, psswd))
            user = User(login, psswd)
        cursor.close()
        self._log("db : user is {}".format(user))
        return user

    def checkDB():
        cursor = self.connexion.cursor()
        query = ("SELECT id, login FROM users")
        cursor.execute(query)
        for (id, login) in cursor:
            sys.stdout.write("id: {} login: {}".format(id, login))
            sys.stdout.write('\n')
            sys.stdout.flush()
        cursor.close()

    def _log(self, message):
        sys.stdout.write(message)
        sys.stdout.write('\n')
        sys.stdout.flush()
