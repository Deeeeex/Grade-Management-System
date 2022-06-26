from src.message import *
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView


def initseaBinding(self, ui, db, cur_user, cur_identity):
    self.ui = ui
    self.db = db

    if cur_identity == 'student':
        # 初始化成绩表格（记录所有该用户参与过的考试成绩）
        self.ui.tableWidget.setRowCount(0)
        # self.ui.custWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格等宽
        data = self.db.execute(
            "select score.e_id, exam.e_date, score.total, score.Chinese, score.Math, score.English from xxp.score, xxp.exam where exam.e_id=score.e_id and s_id=\'" + cur_user + "\';")
        x = 0
        for i in data:
            y = 0
            self.ui.tableWidget.setRowCount(x + 1)
            for j in i:
                self.ui.tableWidget.setItem(x, y, QTableWidgetItem(str(data[x][y])))
                y = y + 1
            x = x + 1
    elif cur_identity == 'teacher':
        self.ui.searchButton.clicked.connect(lambda: updateScore(self, ui, db))
        self.ui.sea_e_Edit.returnPressed.connect(lambda: updateScore(self, ui, db))


def updateScore(self, ui, db):
    e_id = self.ui.sea_e_Edit.text()
    self.ui.tableWidget_2.setRowCount(0)
    # self.ui.custWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格等宽
    data = self.db.execute(
        "select user.u_id, user.u_ide, score.total, score.Chinese, score.Math, score.English from xxp.score, xxp.user where user.u_id = score.s_id and score.e_id=\'" + e_id + "\';")
    x = 0
    for i in data:
        y = 0
        self.ui.tableWidget_2.setRowCount(x + 1)
        for j in i:
            self.ui.tableWidget_2.setItem(x, y, QTableWidgetItem(str(data[x][y])))
            y = y + 1
        x = x + 1
