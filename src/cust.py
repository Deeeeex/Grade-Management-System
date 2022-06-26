from src.message import *
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

def initCustBinding(self, ui, db):
    self.ui = ui
    self.db = db
    self.ui.addCustBtn.clicked.connect(lambda : addCust(self, ui, db))
    self.ui.delCustBtn.clicked.connect(lambda : delCust(self, ui, db))
    self.ui.updtCustBtn.clicked.connect(lambda : updateCust(self, ui, db))
    self.ui.searchCustBtn.clicked.connect(lambda : searchCust(self, ui, db))

# SECTION 1
def addCust(self, ui, db):
    self.ui = ui
    self.db = db
    cuName = self.ui.nameLineEdit.text()
    cuId = self.ui.idLineEdit.text()
    cuTel = self.ui.telLineEdit.text()
    cuAddr = self.ui.addrLineEdit.text()
    coName = self.ui.cNameLineEdit.text()
    coTell = self.ui.cTelLineEdit.text()
    coEmail = self.ui.cEmailLineEdit.text()
    relation = self.ui.cRelaLineEdit.text()
    directorId = self.ui.direIdLineEdit.text()
    serviceType = self.ui.serTypeLineEdit.text()

    if cuId == '':
        critical(self, "请输入客户身份证号！")
        return None
    res = self.db.execute("select * from lab3.Client where c_id = \'" + cuId + '\'')
    # print("select * from lab3.Client where c_id = \'" + cuId + '\'')
    # print(res)
    if res:
        critical(self, "该客户已存在，若要修改信息请点击修改按钮！")
        return None
    if directorId != '':
        res = self.db.execute("select * from lab3.Staff where s_id = \'" + directorId + '\'')
        if not res:
            critical(self, "银行无此员工！")
            return None

    proceStr1 = """create procedure lab3.add_info()\nbegin\n\tstart transaction;"""
    proceStr2 = """\n\tcommit;\nend"""
    t = '\'' + cuId + '\', \'' + cuName + '\', \'' + cuTel + '\', \'' + cuAddr + '\''
    sql = "\n\tinsert into lab3.Client(c_id, c_name, c_tel, c_addr) values(" + t + ");"
    # self.db.execute("insert into lab3.Client(c_id, c_name, c_tel, c_addr) values(" + t + ")")

    t = '\'' + cuId + '\', \'' + coName + '\', \'' + coTell + '\', \'' + coEmail + '\', \'' + relation + '\''
    sql += "\n\tinsert into lab3.Contact(c_id, co_name, co_tel, co_email, relation) values(" + t + ");"
    # self.db.execute("insert into lab3.Contact(c_id, co_name, co_tel, co_email, relation) values(" + t + ")")


    sql +="\n\tif not exists(select * from lab3.Service where c_id = \'" + cuId + "\' and s_id = \'" + directorId + "\' and s_type = \'" + serviceType + "\') then"
    t = '\'' + directorId + '\', \'' + cuId + '\', \'' + serviceType + '\''
    sql += "\n\t\tinsert into lab3.Service(s_id, c_id, s_type) values(" + t + ");\n\tend if;"

    # sql += "\n\tinsert into lab3.Service(s_id, c_id, s_type) values(" + t + ")"
    # self.db.execute("insert into lab3.Service(s_id, c_id, s_type) values(" + t + ")")


    self.db.execute("drop procedure if exists lab3.add_info;")
    # print(proceStr1 + sql + proceStr2)
    self.db.execute(proceStr1 + sql + proceStr2)
    self.db.execute("call lab3.add_info();")

    updateCTable(self, ui, db)

# SECTION 2
def delCust(self, ui, db):
    self.ui = ui
    self.db = db
    cuName = self.ui.nameLineEdit.text()
    cuId = self.ui.idLineEdit.text()
    cuTel = self.ui.telLineEdit.text()
    cuAddr = self.ui.addrLineEdit.text()
    coName = self.ui.cNameLineEdit.text()
    coTell = self.ui.cTelLineEdit.text()
    coEmail = self.ui.cEmailLineEdit.text()
    relation = self.ui.cRelaLineEdit.text()
    directorId = self.ui.direIdLineEdit.text()
    serviceType = self.ui.serTypeLineEdit.text()

    dropProcedure = "drop procedure if exists lab3.drop_info;"
    callProcedure = "call lab3.drop_info();"
    proceStr1 = """create procedure lab3.drop_info()\nbegin\n\tstart transaction;\n\tset FOREIGN_KEY_CHECKS = 0;"""
    proceStr2 = """\n\tset FOREIGN_KEY_CHECKS=1;\n\tcommit;\nend"""


    # 删除客户，其对应的联系人也会被删除
    if cuName != '' or cuId != '' or cuTel != '' or cuAddr != '':
        # sql = '\n\tdelete FROM lab3.Client where'
        delIdStr = 'select c_id from lab3.Client where'
        cond = 0
        if cuName != '':
            t = ' c_name = \'' + cuName + '\''
            # sql += t
            delIdStr += t
            cond = 1
        if cuId != '':
            if cond == 1:
                t = ' and c_id = \'' + cuId + '\''
            else:
                t = ' c_id = \'' + cuId + '\''
                cond = 1
            # sql += t
            delIdStr += t
        if cuTel != '':
            if cond == 1:
                t = ' and c_tel = \'' + cuTel + '\''
            else:
                t = ' c_tel = \'' + cuTel + '\''
                cond = 1
            # sql += t
            delIdStr += t
        if cuAddr != '':
            if cond == 1:
                t = ' and c_addr = \'' + cuAddr + '\''
            else:
                t = ' c_addr = \'' + cuAddr + '\''
            # sql += t
            delIdStr += t

        delId = self.db.execute(delIdStr)
        # sql += ";"
        sql = ''
        for idTuple in delId:
            for id in idTuple:
                res1 = self.db.execute("select * from lab3.own where c_id = \'" + id + '\';')
                res2 = self.db.execute("select * from lab3.transaction where c_id = \'" + id + '\';')
                # print('res1:', res1, 'res2:', res2)
                if res1 or res2:
                    critical(self, "不允许删除存在关联账户或者贷款记录的客户！")
                    return None
                sql += '\n\tdelete FROM lab3.Client where c_id = \'' + str(id) + '\';'
                sql += '\n\tdelete FROM lab3.Contact where c_id = \'' + str(id) + '\';'

        # print(proceStr1 + sql + proceStr2)
        self.db.execute(dropProcedure)
        self.db.execute(proceStr1 + sql + proceStr2)
        self.db.execute(callProcedure)


    elif coName != '' or coTell != '' or coEmail != '' or relation != '':
        sql = '\n\tdelete FROM lab3.Contact where'
        delIdStr = 'select c_id from lab3.Client where'
        cond = 0
        if coName != '':
            t = ' co_name = \'' + coName + '\''
            sql += t
            delIdStr += t
            cond = 1
        if coTell != '':
            if cond == 1:
                t = ' and co_tel = \'' + coTell + '\''
            else:
                t = ' co_tel = \'' + coTell + '\''
                cond = 1
            sql += t
            delIdStr += t
        if coEmail != '':
            if cond == 1:
                t = ' and email = \'' + coEmail + '\''
            else:
                t = ' email = \'' + coEmail + '\''
                cond = 1
            sql += t
            delIdStr += t
        if relation != '':
            if cond == 1:
                t = ' and relation = \'' + relation + '\''
            else:
                t = ' relation = \'' + relation + '\''
            sql += t
            delIdStr += t
        sql += ';'
        self.db.execute(dropProcedure)
        self.db.execute(proceStr1 + sql + proceStr2)
        self.db.execute(callProcedure)

    # 删除客户信息不会删除掉服务信息（要算员工的业绩），除非指定要删除
    if directorId != '' or serviceType != '':
        sql = '\n\tdelete FROM lab3.Service where'
        cond = 0
        if cuId != '':
            sql += ' c_id = \'' + cuId + '\''
            cond = 1
        if directorId != '':
            if cond == 1:
                sql += ' and s_id = \'' + directorId + '\''
            else:
                sql += ' s_id = \'' + directorId + '\''
                cond = 1
        if serviceType != '':
            if cond == 1:
                sql += ' and s_type = \'' + serviceType + '\''
            else:
                sql += ' s_type = \'' + serviceType + '\''
        sql += ';'
        self.db.execute(dropProcedure)
        self.db.execute(proceStr1 + sql + proceStr2)
        self.db.execute(callProcedure)

    updateCTable(self, ui, db)

# SECTION 3
# 根据客户id修改信息，客户id必填
def updateCust(self, ui, db):
    self.ui = ui
    self.db = db
    cuName = self.ui.nameLineEdit.text()
    cuId = self.ui.idLineEdit.text()
    cuTel = self.ui.telLineEdit.text()
    cuAddr = self.ui.addrLineEdit.text()
    coName = self.ui.cNameLineEdit.text()
    coTell = self.ui.cTelLineEdit.text()
    coEmail = self.ui.cEmailLineEdit.text()
    relation = self.ui.cRelaLineEdit.text()
    directorId = self.ui.direIdLineEdit.text()
    serviceType = self.ui.serTypeLineEdit.text()
    if cuId == '':
        warning(self, "请输入客户身份证号")
        return None
    if cuName != '' or cuTel != '' or cuAddr != '':
        sql = 'update lab3.Client set'
        cond = 0
        if cuName != '':
            sql += ' c_name = \'' + cuName + '\''
            cond = 1
        if cuTel != '':
            if cond == 1:
                sql += ', c_tel = \'' + cuTel + '\''
            else:
                sql += ' c_tel = \'' + cuTel + '\''
                cond = 1
        if cuAddr != '':
            if cond == 1:
                sql += ', c_addr = \'' + cuAddr + '\''
            else:
                sql += ' c_addr = \'' + cuAddr + '\''
        sql += ' where c_id = \'' + cuId + '\''
        self.db.execute(sql)

    if coName != '' or coTell != '' or coEmail != '' or relation != '':
        sql = 'update lab3.Contact set'
        cond = 0
        if coName != '':
            sql += ' co_name = \'' + coName + '\''
            cond = 1
        if coTell != '':
            if cond == 1:
                sql += ', co_tel = \'' + coTell + '\''
            else:
                sql += ' co_tel = \'' + coTell + '\''
                cond = 1
        if coEmail != '':
            if cond == 1:
                sql += ', email = \'' + coEmail + '\''
            else:
                sql += ' email = \'' + coEmail + '\''
                cond = 1
        if relation != '':
            if cond == 1:
                sql += ', relation = \'' + relation + '\''
            else:
                sql += ' relation = \'' + relation + '\''
        sql += ' where c_id = \'' + cuId + '\''
        self.db.execute(sql)

    if directorId != '' or serviceType != '':
        sql = 'update lab3.Service set'
        cond = 0
        if directorId != '':
            sql += ' s_id = \'' + directorId + '\''
            cond = 1
        if serviceType != '':
            if cond == 1:
                sql += ', s_type = \'' + serviceType + '\''
            else:
                sql += ' s_type = \'' + serviceType + '\''
        sql += ' where c_id = \'' + cuId + '\''
        self.db.execute(sql)

    updateCTable(self, ui, db)

# SECTION 4
def searchCust(self, ui, db):
    self.ui = ui
    self.db = db
    self.ui.custWidget.setRowCount(0)
    # self.ui.custWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置表格等宽
    data = self.db.execute("""select lab3.Client.c_name, lab3.Client.c_id, lab3.Client.c_tel, lab3.Client.c_addr, lab3.Contact.co_name, 
                            lab3.Contact.co_tel, lab3.Contact.co_email, lab3.Contact.relation, lab3.Service.s_id, lab3.Service.s_type
                            from lab3.Client, lab3.Contact, lab3.Service
                            where lab3.Service.c_id = lab3.Client.c_id and lab3.Service.c_id = lab3.Contact.c_id;""")

    x = 0
    for i in data:
        y = 0
        self.ui.custWidget.setRowCount(x + 1)
        for j in i:
            self.ui.custWidget.setItem(x, y, QTableWidgetItem(str(data[x][y])))
            y = y + 1
        x = x + 1


def updateCTable(self, ui, db):
    # 若本来table就有内容显示，则更新显示的内容
    if ui.custWidget.rowCount() > 0:
        searchCust(self, ui, db)
