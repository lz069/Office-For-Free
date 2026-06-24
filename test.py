# test_web.py
import os
import sys

# 一定要在导入 PySide6 之前
os.environ["QTWEBENGINE_DISABLE_GPU"] = "1"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"
os.environ["QT_QUICK_BACKEND"] = "software"

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebEngine Test")
        self.resize(900, 700)

        self.view = QWebEngineView(self)
        self.setCentralWidget(self.view)

        # 随便打开一个网页测试
        self.view.load(QUrl("https://www.qt.io"))


if __name__ == "__main__":
    # 某些环境下需要手动 initialize
    #QtWebEngine.initialize()

    app = QApplication(sys.argv)
    win = TestWindow()
    win.show()
    sys.exit(app.exec())
