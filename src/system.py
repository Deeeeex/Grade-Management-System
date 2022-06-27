from ui.system_ui import Ui_system
from src.search import *
from src.register import *
from src.analysis import *
from src.output import *
from src.input import *
from src.message import *
from src.database import Database
from PyQt5.QtWidgets import QDialog, QMainWindow, QLineEdit, QTableWidgetItem, QHeaderView

cur_user = ''
cur_identity = ''


class System(QMainWindow):
    ui = None
    db = Database()
    dbName = None

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_system()
        self.ui.setupUi(self)
        # self.db = Database()

        self.initBtnColor()

        self.initHomeBinding()
        initRegiBinding(self, self.ui, self.db)
        self.setStuBtnEnabled(False)
        self.setTecBtnEnabled(False)
        # self.initPageBinding()  # 不能写在__init__里面，那时候还没有连接数据库

        self.show()

    def initBtnColor(self):
        btns = [self.ui.homeBtn, self.ui.seaBtn, self.ui.anaBtn, self.ui.oupBtn, self.ui.inpBtn, self.ui.regiBtn]
        for b in btns:
            b.setStyleSheet(
                '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')

    def initHomeBinding(self):
        # 设置pushbutton和stackedWidget的连接
        self.ui.homeBtn.clicked.connect(self.homeBtnFun)
        self.ui.regiBtn.clicked.connect(self.regiBtnFun)
        self.ui.seaBtn.clicked.connect(self.seaBtnFun)
        self.ui.anaBtn.clicked.connect(self.anaBtnFun)
        self.ui.oupBtn.clicked.connect(self.oupBtnFun)
        self.ui.inpBtn.clicked.connect(self.inpBtnFun)

        # 设置首页按钮的连接
        self.ui.loginBtn.clicked.connect(self.login)
        self.ui.logOutBtn.clicked.connect(self.logOut)
        self.ui.pwdLineEdit.returnPressed.connect(self.login)

    def initPageBinding(self):
        global cur_identity
        global cur_user
        initseaBinding(self, self.ui, self.db, cur_user, cur_identity)
        initAnaBinding(self, self.ui, self.db, cur_user, cur_identity)
        initOupBinding(self, self.ui, self.db)
        initInpBinding(self, self.ui, self.db)

    def login(self):
        self.ui.pwdLineEdit.setEchoMode(QLineEdit.Password)
        username = self.ui.userLineEdit.text()
        password = self.ui.pwdLineEdit.text()
        identity = self.db.execute(
            "select u_ide from xxp.user where u_id = \'" + username + '\'' + "and u_pwd = \'" + password + "\'")
        global cur_user
        global cur_identity
        if not identity:
            critical(self, "登陆失败")
        elif cur_user:
            critical(self, "请先退出当前用户")
        else:
            cur_user = username
            cur_identity = identity[0][0]
            # print(identity[0][0])
            if identity[0][0] == 'student':
                self.setStuBtnEnabled(True)
            else:
                self.setTecBtnEnabled(True)
            information(self, "登陆成功")
            self.initPageBinding()

    def logOut(self):
        # 设置按钮不可点击
        self.setStuBtnEnabled(False)
        self.setTecBtnEnabled(False)
        global cur_user
        cur_user = ''

    def setStuBtnEnabled(self, flag):
        self.ui.seaBtn.setEnabled(flag)
        self.ui.anaBtn.setEnabled(flag)
        # self.ui.oupBtn.setEnabled(flag)
        # self.ui.inpBtn.setEnabled(flag)

    def setTecBtnEnabled(self, flag):
        self.ui.seaBtn.setEnabled(flag)
        self.ui.anaBtn.setEnabled(flag)
        self.ui.oupBtn.setEnabled(flag)
        self.ui.inpBtn.setEnabled(flag)

    def setBtnColor(self, btn):
        btns = [self.ui.homeBtn, self.ui.seaBtn, self.ui.anaBtn, self.ui.oupBtn, self.ui.inpBtn, self.ui.regiBtn]
        btns.remove(btn)
        for b in btns:
            b.setStyleSheet(
                '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        btn.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

    def homeBtnFun(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.setBtnColor(self.ui.homeBtn)

    def regiBtnFun(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.setBtnColor(self.ui.regiBtn)

    def seaBtnFun(self):
        global cur_identity
        if cur_identity == 'student':
            self.ui.stackedWidget.setCurrentIndex(2)
        elif cur_identity == 'teacher':
            self.ui.stackedWidget.setCurrentIndex(6)
        self.setBtnColor(self.ui.seaBtn)

    def anaBtnFun(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.setBtnColor(self.ui.anaBtn)

    def oupBtnFun(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.setBtnColor(self.ui.oupBtn)

    def inpBtnFun(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.setBtnColor(self.ui.inpBtn)
