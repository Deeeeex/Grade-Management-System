from src.message import *
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

def initRegiBinding(self, ui, db):
    self.ui = ui
    self.db = db
    self.ui.registerBtn.clicked.connect(lambda : addUser(self, ui, db))

def addUser(self, ui, db):
    u_id = self.ui.idEdit.text()
    u_name = self.ui.nameEdit.text()
    u_class = self.ui.classEdit.text()
    regiCode = self.ui.regiCodeEdit.text()
    u_pwd = self.ui.passwordEdit.text()
    u_ide = ''
    if regiCode == 'stu':
        u_ide = 'student'
    elif regiCode == 'tea':
        u_ide = 'teacher'
    t = '\'' + u_id + '\', \'' + u_pwd + '\', \'' + u_ide + '\', \'' + u_class + '\''
    sql = "insert into xxp.user(u_id, u_pwd, u_ide, u_class) values(" + t + ");"
    self.db.execute(sql)
    critical(self, "注册成功")
