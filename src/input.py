from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem
from src.message import *


def initInpBinding(self, ui, db):
    self.ui = ui
    self.db = db
    self.ui.submitButton.clicked.connect(lambda: addScore(self, ui, db))


def addScore(self, ui, db):
    e_id = self.ui.e_id_Edit.text()
    s_id = self.ui.s_id_Edit.text()
    Chinese = self.ui.Chinese_Edit.text()
    Math = self.ui.Math_Edit.text()
    English = self.ui.English_Edit.text()
    try:
        total = int(Chinese) + int(Math) + int(English)
        total = str(total)
    except:
        total = '0'
    if e_id == '':
        critical(self, "请输入考试ID")
        return None
    if s_id == '':
        critical(self, "请输入考生ID")
        return None
    exa = self.db.execute("select * from xxp.exam where e_id = \'" + e_id + '\'')
    if not exa:
        critical(self, "请检查考试ID")
        return None
    stu = self.db.execute("select * from xxp.user where u_id = \'" + s_id + '\'')
    if not stu:
        critical(self, "请检查考生ID")
        return None
    t = '\'' + s_id + '\', \'' + e_id + '\', \'' + total + '\', \'' + Chinese + '\', \'' + Math + '\', \'' + English + '\''
    sql = "insert into xxp.score(s_id, e_id, total, Chinese, Math, English) values(" + t + ");"
    try:
        self.db.execute(sql)
        critical(self, "录入成功")
    except:
        print("重复录入！")
