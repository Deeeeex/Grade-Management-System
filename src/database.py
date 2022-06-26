# -*- coding: UTF-8 -*-
import pymysql
from src.message import *


class Database:
    __db = None
    __error = None

    def __init__(self) -> None:
        try:
            self.__db = pymysql.connect(host="localhost", user="root", password="123456", database="xxp",
                                        charset="utf8")
        except pymysql.Error as e:
            critical(self, e)
            print(e)
            self.__error = e
            self.__db = None
        pass

    def __del__(self):
        self.close()

    def execute(self, sql):
        try:
            cursor = self.__db.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            self.__db.commit()
            return res

        except pymysql.Error as e:
            print(e)
            self.__error = e[1]
            self.__db.rollback()
            return None

    def executeProc(self, sql, procName, param1, param2, outParam1, outParam2):
        try:
            cursor = self.__db.cursor()
            cursor.callproc(procName, (param1, param2, outParam1, outParam2))
            cursor.execute(sql)
            res = cursor.fetchall()
            self.__db.commit()
            return res

        except pymysql.Error as e:
            print(e)
            self.__error = e[1]
            self.__db.rollback()
            return None

    def executeProcT(self, procName, param1, param2):
        try:
            cursor = self.__db.cursor()
            cursor.callproc(procName, (param1, param2))
            # cursor.execute(sql)
            res = cursor.fetchall()
            self.__db.commit()
            return res

        except pymysql.Error as e:
            print(e)
            self.__error = e[1]
            self.__db.rollback()
            return None

    def close(self):
        return
        # if self.__db is not None:
        #     self.__db.close()

    def getError(self):
        return self.__error

    def isConnected(self):
        return self.__db is not None


if __name__ == "__main__":
    # 测试数据库连接
    db = Database()

    tables = db.execute("SHOW TABLES;")
    if tables is not None:
        for table in tables:
            count = db.execute("SELECT count(*) FROM " + table[0])
            print(table[0], count[0][0])
