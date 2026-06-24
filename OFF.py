# @Author: Zhi Li
# @Date:   2024-06-10 10:00:00
# @Softeware Name: Office For Free(Freedom) (OFF)
# @Description: A free and open-source office suite.

import sys,os

from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QMenuBar, QProgressBar, QPushButton, QToolBar, QStatusBar, QTabWidget, QHBoxLayout, QStackedWidget
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QTimer, QUrl, Slot
from OFFclass import CreateMenubar, sidebar
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtPdf import QPdfDocument
from PySide6.QtWebEngineCore import QWebEngineSettings
import fitz
from OFFclass import sidebar




class OFFGUI(QMainWindow):

    #initialize the main window
    def __init__(self):
        
        super().__init__()
        
        self.setWindowTitle("Office For Free (OFF)")
        self.setGeometry(400, 250, 1200, 800)
        #label = QLabel("Welcome to Office For Free (OFF)!", self)
        #label.setGeometry(200, 250, 400, 100)
        self.Tabwidget()
        self.extract_toolbar()
        self.mainsetupmenubar()
        #self.mainrightsidebar()
        
        self.mainstatusbar()
        #self.maintoolbar()
        #if self.returnselected:
        #    self.statusbar.showMessage(Path(self.returnselected), 5000)

        #else:
        #    self.statusbar.showMessage("No file selected", 5000)
        

        #self.browser = QWebEngineView()
        #self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        #self.browser.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        #self.browser.setUrl(QUrl("https://www.google.com")
        #url=QUrl.fromLocalFile("C:/Users/MSI/Desktop/pdf-wangtest.pdf")
        #url=QUrl.fromLocalFile("C:/Users/MSI/Desktop/Ultrafast_Optics.pdf")
        #self.browser.load(url)
        #self.browser.load(QUrl("file:///C:/Users/MSI/Desktop/pdf-wangtest.pdf"))
        #self.setCentralWidget(self.browser)

        #self.pdfviewer(r"C:/Users/MSI/Desktop/Ultrafast_Optics.pdf")
        #self.viewer = pdfviewer(self.selected_files)
        #self.setCentralWidget(self.viewer)
        
        self.progressbar()
        self.statusbar.addPermanentWidget(self.progress)
        self.showMaximized()
        






    #setup menubar(top menubar)
    def mainsetupmenubar(self):

        self.menubar = CreateMenubar(self)
        self.menubar.setup_menubar()

    #def mainrightsidebar(self):




    #def maintoolbar(self):
        #self.maintoolbar = QToolBar()
       # self.toolbar = self.addToolBar(self.maintoolbar)
        #self.toolbar.isMovable
        #self.toolbar.isFloatable
        #self.toolbar.setMovable(False)
        #self.toolbar.setFloatable(False)

    def Tabwidget(self):
        self.Tabwidegts = QTabWidget()
        self.Tabwidegts.setTabsClosable(True)
        self.Tabwidegts.setMovable(True)
        self.Tabwidegts.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.Tabwidegts)
        self.rightsidebar = sidebar(self)
        self.rightsidebar.setup_rightsidebar()
        self.Tabwidegts.currentChanged.connect(self.rightsidebar.extract_toolbar_update)



    @Slot(int)
    def close_tab(self, index):
        widget = self.Tabwidegts.widget(index)
        if widget:
            widget.deleteLater()
            self.Tabwidegts.removeTab(index)


    """
    def pdfviewer(self, pdf_path):
        self.viewer = QWebEngineView(self)
        #self.viewer.settings().setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        self.setCentralWidget(self.viewer)
        self.viewer.load(QUrl.fromLocalFile(pdf_path))
        self.viewer.show()
    """
    """
    def pdfviewer(self, pdf_path):
        self.pdf_document = QPdfDocument(self)
        self.pdf_document.load(pdf_path)
        self.pdf_view = QPdfView(self)
        #self.pdf_view.setGeometry(50, 50, 1200, 1200)
        self.setCentralWidget(self.pdf_view)
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdf_view.setZoomMode(QPdfView.FitToWidth)
        self.pdf_view.setDocument(self.pdf_document)
        self.pdf_view.setZoomMode(QPdfView.FitToWidth)
        #self.pdf_view.show()
    """

    
    def mainstatusbar(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready")
        


    def progressbar(self):
        self.progress = QProgressBar()
        #self.progress.setGeometry(200, 550, 400, 25)
       #self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setMaximumWidth(200)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
       #self.progress.show()

        self.timer = QTimer()
        #self.timer.timeout.connect(self.handleTimer)
        self.timer.start(100)
        self.step = 0
    

    
    def extract_toolbar(self):
        self.toolbar_extract = sidebar(self)
        self.extract_toolbar_tool = QToolBar("Extract Toolbar")
        self.addToolBar(Qt.TopToolBarArea, self.extract_toolbar_tool)
        self.extract_widget = QWidget()
        self.extract_toolbar_tool.addWidget(self.extract_widget)
        self.extract_layout = QHBoxLayout(self.extract_widget)
        self.extract_layout.setSpacing(10)
        self.extract_toolbar_tool.setMovable(False)
        self.extract_toolbar_tool.setFloatable(False)
        self.extract_layout.addStretch()
        self.toolbar_extract.extract_pages_button()
        self.toolbar_extract.extract_close_button()
        self.extract_layout.addStretch()
        self.extract_toolbar_tool.setVisible(False)
        #self.extract_toolbar_tool.setVisible(False)











if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "ICON", "OFFicon.png")))
    window = OFFGUI()
    window.show()
    sys.exit(app.exec())