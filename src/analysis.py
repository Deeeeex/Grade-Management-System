from enum import Enum
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap
from src.message import *
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView


class Account(Enum):
    savingAcc = 1
    checkingAcc = 2


def initAnaBinding(self, ui, db, cur_user, cur_identity):
    self.ui = ui
    self.db = db
    total_Ana(self, ui, db, cur_user, cur_identity)
    self.ui.total_ana_Button.clicked.connect(lambda: total_Ana(self, ui, db, cur_user, cur_identity))
    self.ui.Chinese_ana_Button.clicked.connect(lambda: Chinese_Ana(self, ui, db, cur_user, cur_identity))
    self.ui.Math_ana_Button.clicked.connect(lambda: Math_Ana(self, ui, db, cur_user, cur_identity))
    self.ui.English_ana_Button.clicked.connect(lambda: English_Ana(self, ui, db, cur_user, cur_identity))


def total_Ana(self, ui, db, cur_user, cur_identity):
    plt.clf()
    data = self.db.execute(
        "select score.e_id,score.total from xxp.score where s_id=\'" + cur_user + "\';")
    data_dict = {}
    for i in data:
        data_dict[i[0]] = i[1]
    # for i, j in zip(x, y):
    #     data_dict[i] = j
    plt.figure(figsize=(9.5, 8))
    plt.title("Total Changing")
    plt.xlabel("Exam ID")
    plt.ylabel("Score")
    x = [i for i in data_dict.keys()]
    y = [i for i in data_dict.values()]
    plt.plot(x, y, label="Total")
    plt.legend()
    plt.savefig('成绩分析.png')

    pix = QPixmap('成绩分析.png')
    self.ui.imgLabel.setPixmap(pix)


def Chinese_Ana(self, ui, db, cur_user, cur_identity):
    plt.clf()
    data = self.db.execute(
        "select score.e_id,score.Chinese from xxp.score where s_id=\'" + cur_user + "\';")
    data_dict = {}
    for i in data:
        data_dict[i[0]] = i[1]

    plt.title("Chinese Changing")
    plt.xlabel("Exam ID")
    plt.ylabel("Score")
    x = [i for i in data_dict.keys()]
    y = [i for i in data_dict.values()]
    plt.plot(x, y, label="Chinese")
    plt.legend()
    plt.savefig('成绩分析.png')

    pix = QPixmap('成绩分析.png')
    self.ui.imgLabel.setPixmap(pix)


def Math_Ana(self, ui, db, cur_user, cur_identity):
    plt.clf()
    data = self.db.execute(
        "select score.e_id,score.Math from xxp.score where s_id=\'" + cur_user + "\';")
    data_dict = {}
    for i in data:
        data_dict[i[0]] = i[1]

    plt.title("Math Changing")
    plt.xlabel("Exam ID")
    plt.ylabel("Score")
    x = [i for i in data_dict.keys()]
    y = [i for i in data_dict.values()]
    plt.plot(x, y, label="Math")
    plt.legend()
    plt.savefig('成绩分析.png')

    pix = QPixmap('成绩分析.png')
    self.ui.imgLabel.setPixmap(pix)


def English_Ana(self, ui, db, cur_user, cur_identity):
    plt.clf()
    data = self.db.execute(
        "select score.e_id,score.English from xxp.score where s_id=\'" + cur_user + "\';")
    data_dict = {}
    for i in data:
        data_dict[i[0]] = i[1]
    plt.title("English Changing")
    plt.xlabel("Exam ID")
    plt.ylabel("Score")
    x = [i for i in data_dict.keys()]
    y = [i for i in data_dict.values()]
    plt.plot(x, y, label="English")
    plt.legend()
    plt.savefig('成绩分析.png')

    pix = QPixmap('成绩分析.png')
    self.ui.imgLabel.setPixmap(pix)
