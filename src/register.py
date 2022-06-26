from src.message import *
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

def initRegiBinding(self, ui, db):
    self.ui = ui
    self.db = db
    # self.ui.addCustBtn.clicked.connect(lambda : addCust(self, ui, db))
    # self.ui.delCustBtn.clicked.connect(lambda : delCust(self, ui, db))
    # self.ui.updtCustBtn.clicked.connect(lambda : updateCust(self, ui, db))
    # self.ui.searchCustBtn.clicked.connect(lambda : searchCust(self, ui, db))