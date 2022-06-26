from PyQt5.QtWidgets import QApplication
from src.system import System
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    system = System()
    sys.exit(app.exec_())
