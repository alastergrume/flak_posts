import math
import sqlite3
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sq1 = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sq1)
            res = self.__cur.fetchall()
            # print(res)
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addPost(self, title, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?)", (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД" + str(e))
            return False

        return True

    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {postId} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД" + str(e))

        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД" + str(e))

        return []

    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f'SELECT COUNT() as `count` FROM users WHERE email LIKE "{email}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким имеменем уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Это из adduser Ошибка добавления пользователей в БД"+str(e))
            return False

        return True

    def getUser(self, user_id):
        print(user_id)
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("getUser Ошибка получения данных из БД "+str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False

