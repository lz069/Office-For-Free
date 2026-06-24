import os, sys, io
from matplotlib import style
from pdf2image import convert_from_path, convert_from_bytes
from pypdf import PdfReader, PdfWriter
from PySide6.QtWidgets import QMainWindow, QApplication, QProgressBar, QFileDialog, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QToolBar,QDockWidget, QWidget, QPushButton, QMenuBar, QStackedWidget, QScrollArea, QToolButton, QListWidget, QGridLayout,QSizePolicy, QListWidgetItem
from PySide6.QtCore import QTimer, Qt, QUrl, Slot, QSize, QCoreApplication
from PySide6.QtGui import QIcon, QAction, QDesktopServices, QPixmap, QImage
from PySide6.QtWebEngineWidgets import QWebEngineView
from pathlib import Path
from PySide6.QtWebEngineCore import QWebEngineSettings
from offviewer import pdfviewer
import pymupdf
from PIL import Image


class CreateMenubar:
    def __init__(self, window):
        self.window = window

    def setup_menubar(self):

        self.menubar = self.window.menuBar()
        self.file_menu = self.menubar.addMenu("File")

        self.open_file = self.file_menu.addAction(QIcon("ICON/openfile.png"), "Open File")
        self.open_file.triggered.connect(self.open_file_dialog)

        self.close_window = self.file_menu.addAction(QIcon("ICON/close.png"), "Close")
        self.close_window.triggered.connect(self.window.close)


        self.edit_menu = self.menubar.addMenu("Edit")
        self.extract_pages = self.edit_menu.addAction(QIcon("ICON/extract.png"), "Extract Pages")
        self.split_file = self.edit_menu.addAction(QIcon("ICON/split.png"), "Split PDF")
        self.merge_file = self.edit_menu.addAction(QIcon("ICON/merge.png"), "Merge PDF")
        
        self.view_menu = self.menubar.addMenu("View")
        self.help_menu = self.menubar.addMenu("Help")
        self.tutorial_action = self.help_menu.addAction(QIcon("ICON/help.png"),"Tutorial")
        self.tutorial_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/lz069/Office-For-Free--Freedom")))
        self.about_action = self.menubar.addMenu("About")
        self.about_OFF = self.about_action.addAction(QIcon("ICON/about.png"), "About OFF")
        self.about_OFF.triggered.connect(self.dialog_about_OFF)
        self.GitHUB_action = self.about_action.addAction(QIcon("ICON/github.png"), "GitHub Repository")
        self.GitHUB_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/lz069/Office-For-Free--Freedom")))
        
        
        self.Contact_action = self.menubar.addMenu("Contact")
        self.contact_action = self.Contact_action.addAction(QIcon("ICON/contact.png"), "Contact Us")
        self.contact_action.triggered.connect(self.dialog_contact)
    
        #self.toggle_sidebar_action = QAction("Toggle Sidebar", self.window)
        #self.toggle_sidebar_action.triggered.connect(self.toggle_sidebar)
        #self.right_widget = QWidget(self.window)
        #layout = QHBoxLayout(self.right_widget)
        #layout.setContentsMargins(0, 0, 0, 0)

        self.toggle_button = QPushButton(QIcon("ICON/switcher.png"), "Toggle Sidebar", self.window)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        #layout.addWidget(self.toggle_button)

        self.menubar.setCornerWidget(self.toggle_button, Qt.TopRightCorner)

        
        #self.window.setMenuBar(self.menubar)

    def open_file_dialog(self):
        self.file_dialog = QFileDialog(self.window)
        self.file_dialog.setWindowTitle("Open File")
        self.file_dialog.setFileMode(QFileDialog.ExistingFiles)
        self.file_dialog.setNameFilter("PDF Files (*.pdf);;All Files (*)")
        self.file_dialog.setViewMode(QFileDialog.Detail)


        if self.file_dialog.exec():
            #self.viewer = [None] * len(self.file_dialog.selectedFiles())
            #self.selected_files = self.file_dialog.selectedFiles()[0]
            
            for i, file in enumerate(self.file_dialog.selectedFiles()):
                current_viewer = pdfviewer(file)
                current_viewer.file_path = file
                current_viewer.extract_enabled = False

                if str(Path(file).name) in [self.window.Tabwidegts.tabText(j) for j in range(self.window.Tabwidegts.count())]:
                    self.window.statusbar.showMessage(f"File '{str(Path(file).name)}' is already opened.", 5000)
                    self.window.Tabwidegts.setCurrentIndex([self.window.Tabwidegts.tabText(j) for j in range(self.window.Tabwidegts.count())].index(str(Path(file).name)))
                    continue

                self.window.Tabwidegts.addTab(current_viewer, str(Path(file).name))
                self.window.progress.setValue(0)

                #self.window.Tabwidegts.tabBar().setTabData(i, str(Path(file)))
                self.window.statusbar.showMessage(str(Path(file)))
            

    """
        if self.file_dialog.exec():
            self.selected_files = self.file_dialog.selectedFiles()[0]
            self.viewer = pdfviewer(self.selected_files)
            self.window.setCentralWidget(self.viewer)
            self.window.statusbar.showMessage(str(Path(self.selected_files)))
                
        else:
        #    self.selected_files = None
        #    self.window.statusbar.showMessage("No file selected")    

    """
    
    
    #def dialog_tutorial(self):

    
    def dialog_about_OFF(self):
        self.about_dialog = QDialog(self.window)
        self.about_dialog.setWindowTitle("About")
        layout = QVBoxLayout(self.about_dialog)
        about_label = QLabel("Office For Free v1.0\nDeveloped by Zhi Li\n© 2025 All rights reserved.", self.about_dialog)
        about_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(about_label)
        self.about_dialog.setLayout(layout)
        self.about_dialog.setWindowModality(Qt.ApplicationModal)
        self.about_dialog.exec()

    def dialog_contact(self):
        self.contact_dialog = QDialog(self.window)
        self.contact_dialog.setWindowTitle("Contact Us")
        layout = QVBoxLayout(self.contact_dialog)
        contact_label = QLabel("For support, please contact us:\nAuthor: Zhi Li\nEmail: z.li@ifw-dresden.de\nLeibniz-Institut für Festkörper- und Werkstoffforschung Dresden e. V.\nHelmholtzstraße 20, 01069 Dresden, Germany", self.contact_dialog)
        contact_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(contact_label)
        self.contact_dialog.setLayout(layout)
        self.contact_dialog.setWindowModality(Qt.ApplicationModal)
        self.contact_dialog.exec()
    
    def toggle_sidebar(self):
        if self.window.rightsidebar.sidebar.isVisible():
            self.window.rightsidebar.sidebar.hide()
        else:
            self.window.rightsidebar.sidebar.show()


    """    
    class TootbarTop:
        def __init__(self, window):
            self.window = window

        def setup_toolbar(self):
            self.toolbar = self.window.addToolBar("Main Toolbar")

            self.split_file = QAction(QIcon.fromTheme("document-open"), "Open File", self.window)
            self.split_file.triggered.connect(self.window.menubar.open_file_dialog)
            self.toolbar.addAction(self.split_file)

            self.toolbar.addSeparator()

            self.close_tab_action = QAction(QIcon.fromTheme("window-close"), "Close Tab", self.window)
            self.close_tab_action.triggered.connect(self.close_current_tab)
            self.toolbar.addAction(self.close_tab_action)

        def close_current_tab(self):
            current_index = self.window.Tabwidegts.currentIndex()
            if current_index != -1:
                widget = self.window.Tabwidegts.widget(current_index)
                if widget:
                    widget.deleteLater()
                    self.window.Tabwidegts.removeTab(current_index)
    """

#expandable right sidebar
class sidebar:
    def __init__(self, window):
        self.window = window

    def setup_rightsidebar(self):


        self.sidebar = QDockWidget("Tool Bar", self.window)
        self.window.addDockWidget(Qt.RightDockWidgetArea, self.sidebar)
        #self.sidebar.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)
        self.sidebar.setFeatures(QDockWidget.DockWidgetMovable)
        self.split_widget = QWidget(self.window)
        self.sidebar.setWidget(self.split_widget)
        layout = QVBoxLayout(self.split_widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        self.withdraw_button = QToolButton(self.split_widget)
        self.withdraw_button.setFixedSize(100, 80)
        self.withdraw_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.withdraw_button.setIcon(QIcon("ICON/extract.png"))
        self.withdraw_button.setIconSize(QSize(42, 42))
        self.withdraw_button.setText("Extract Pages")
        self.withdraw_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.withdraw_button.clicked.connect(self.stack_extract_pages)
        self.split_button = QToolButton(self.split_widget)
        self.split_button.setFixedSize(100, 80)
        self.split_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.split_button.setIcon(QIcon("ICON/split.png"))
        self.split_button.setIconSize(QSize(42, 42))
        self.split_button.setText("Split PDF")
        self.split_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.merge_button = QToolButton(self.split_widget)
        self.merge_button.setFixedSize(100, 80)
        self.merge_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.merge_button.setIcon(QIcon("ICON/merge.png"))
        self.merge_button.setIconSize(QSize(42, 42))
        self.merge_button.setText("Merge PDF")
        self.merge_button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        layout.addWidget(self.withdraw_button, alignment=Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.split_button, alignment=Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.merge_button, alignment=Qt.AlignHCenter | Qt.AlignTop)

        layout.addStretch()




    def stack_extract_pages(self):
        # 当前 tab 的 pdfviewer
        self.window.viewer = self.window.Tabwidegts.currentWidget()
        file_path = getattr(self.window.viewer, "file_path", None)
        print("Disposed file path:", file_path)
        idx = self.window.Tabwidegts.currentIndex()
        title = self.window.Tabwidegts.tabText(idx)
        print("Current tab index:", idx)


        if not file_path:
            print("⚠ 当前 viewer 没有 file_path，无法分页预览")
            return



        # 如果当前 tab 已经是 stack，可以复用
        if isinstance(self.window.viewer, QStackedWidget):
            stack = self.window.viewer
        else:
            stack = QStackedWidget()
            self.window.Tabwidegts.removeTab(idx)
            stack.addWidget(self.window.viewer)  # index 0：原 PDF 页面

            # 用 stack 替换当前 tab 内容
            #title = self.window.Tabwidegts.tabText(idx)

            self.window.Tabwidegts.insertTab(idx, stack, title)
            self.window.Tabwidegts.setCurrentIndex(idx)
            #self.window.Tabwidegts.extract_enabled = True


        # 生成缩略图页面（index 1）
        thumb_page = self.create_thumbnail_page(file_path)
        stack.addWidget(thumb_page)
        stack.setCurrentIndex(1)
        self.window.Tabwidegts.currentWidget().extract_enabled = True
        self.extract_toolbar_update()
        #print(self.window.Tabwidegts.currentIndex())


    def extract_toolbar_update(self):
        w = self.window.Tabwidegts.currentWidget()
        if w is None:
            self.window.extract_toolbar_tool.hide()
            return
        enabled = getattr(w, "extract_enabled", False)
        self.window.extract_toolbar_tool.setVisible(enabled)
        #print(f"Extract toolbar visible: {enabled}")

    def create_thumbnail_page(self, file_path):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.window.container = QListWidget()
        self.window.container.setSelectionMode(QListWidget.ExtendedSelection)
        self.window.container.setWrapping(True)
        self.window.container.setResizeMode(QListWidget.Adjust)
        self.window.container.setViewMode(QListWidget.IconMode)
        self.window.container.setSpacing(10)
        self.window.container.setIconSize(QSize(190, 220))  

        with open(file_path, "rb") as f:
            pdf_file = pymupdf.open(f)
        
        self._thumb_buffers = []
        total_pages = len(pdf_file)
        self.window.progress.setRange(0, total_pages)
        self.window.progress.setValue(0)


        for page_index in range(len(pdf_file)):
            page = pdf_file.load_page(page_index)

            # 这里可以根据需要调整 DPI
            mat = pymupdf.Matrix(2, 2)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            img_bytes = img_buffer.getvalue()
            self._thumb_buffers.append(img_bytes)
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes)
            icon = QIcon(pixmap.scaledToWidth(190, Qt.SmoothTransformation))
            item = QListWidgetItem(f"Page {page_index + 1}", self.window.container)
            item.setData(Qt.UserRole, page_index)
            item.setIcon(icon)
            item.setSizeHint(QSize(200, 250))  # 留点空间放文字
            self.window.container.addItem(item)
            self.window.progress.setValue(page_index + 1)
            QCoreApplication.instance().processEvents()
        
        self.window.container.itemDoubleClicked.connect(self.double_click_thumbnail)
        scroll_area.setWidget(self.window.container)
        
        return scroll_area

        

        #pil_images = convert_from_bytes(pdf_bytes, dpi=150)

  
    
        #layout = QHBoxLayout(container)
        #layout.setContentsMargins(0, 0, 0, 0)
        #layout.setSpacing(5)
       # layout.setSpacing(1)

        # 用一个列表保存 bytes，确保它们不会被回收
        #self._thumb_buffers = []
    """
        for img in pil_images:
            img = img.convert("RGBA")       # 统一用 RGBA，简单可靠
            w, h = img.size
            buf = img.tobytes("raw", "RGBA")

            self._thumb_buffers.append(buf)    # ★ 把 buffer 存起来，防止被 GC 回收

            qimg = QImage(buf, w, h, w * 4, QImage.Format_RGBA8888)
            # 为了再保险，也可以加 .copy() 强制拷贝一份 Qt 自己的内存：
            # qimg = QImage(buf, w, h, w * 4, QImage.Format_RGBA8888).copy()

            #pixmap = QPixmap.fromImage(qimg).scaledToWidth(
            #    400, Qt.SmoothTransformation
            #)
            lbl = QListWidgetItem(container)
            lbl.setIcon(QIcon(QPixmap.fromImage(qimg).scaledToWidth(200, Qt.SmoothTransformation)))
            lbl.setSizeHint(QSize(200,250))  # 留点空间放文字   
            container.addItem(lbl)

        scroll_area.setWidget(container)
        return scroll_area
    """


    
    def extract_close_button(self):
        self.extract_close = QPushButton("Close", self.window)
        self.extract_close.clicked.connect(self.close_extract_pages)
        #self.extract_close.setFixedSize(150, 40)
        #self.extract_close.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.window.extract_layout.addWidget(self.extract_close)

    def close_extract_pages(self):
        idx = self.window.Tabwidegts.currentIndex()
        stack_widget = self.window.Tabwidegts.currentWidget()
        if isinstance(stack_widget, QStackedWidget):
            original_viewer = stack_widget.widget(0)
            self.window.Tabwidegts.removeTab(idx)
            self.window.Tabwidegts.insertTab(idx, original_viewer, str(Path(getattr(original_viewer, "file_path")).name))
            self.window.Tabwidegts.setCurrentIndex(idx)
            self.window.extract_toolbar_tool.hide()
        return original_viewer
    


    def double_click_thumbnail(self, item):
        page_number = item.data(Qt.UserRole)
        print(f"Double clicked on page {page_number + 1}")
        stack = self.window.Tabwidegts.currentWidget()
        if isinstance(stack, QStackedWidget):
            viewer =self.close_extract_pages()
            #stack.setCurrentIndex(0)

            
            js = f"""
        PDFViewerApplication.pdfViewer.currentPageNumber = {page_number + 1};
       
                """
            viewer.page().runJavaScript(js)

    def extract_pages_button(self):
        self.extract_pages_btn = QPushButton("Save Selected Pages")
        self.extract_pages_btn.clicked.connect(self.save_selected_pages_as_pdf)
        self.window.extract_layout.addWidget(self.extract_pages_btn)


    


    def save_selected_pages_as_pdf(self):
        selected_items = self.window.container.selectedItems()
        selected_pages = [item.data(Qt.UserRole) for item in selected_items]
        selected_pages.sort()
        if not selected_pages:
            print("No pages selected.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self.window, "Save Selected Pages As", "", "PDF Files (*.pdf);;All Files (*)")
        if not file_path:
            return

        #self.viewer = self.window.Tabwidegts.currentWidget()
        original_file_path = getattr(self.window.viewer, "file_path", None)
        if not original_file_path:
            print("Original file path not found.")
            return

        pdf_file = pymupdf.open(original_file_path)
        pages = [pdf_file.load_page(i) for i in selected_pages]
        new_pdf = pymupdf.open()
        for page in pages:
            new_pdf.insert_pdf(pdf_file, from_page=page.number, to_page=page.number)
        new_pdf.save(file_path)
        new_pdf.close()
        print(f"Selected pages saved to {file_path}")
    

    
    """     
    def stack_extract_pages(self):
        file_disposed = self.window.Tabwidegts.currentWidget()
        file_path_disposed = getattr(file_disposed, 'file_path')
        print(f"Disposed file path: {file_path_disposed}")
        idx = self.window.Tabwidegts.currentIndex()
        
        self.stack_extract_widget = QStackedWidget(self.window)

        self.stack_extract_widget.addWidget(file_disposed)
        with open(file_path_disposed, "rb") as f_path_disposed:
            self.pdf_document_disposed = f_path_disposed.read()
        self.imagesenu = convert_from_bytes(self.pdf_document_disposed)
        scroll_area = QScrollArea(self.window)
        scroll_area.setWidgetResizable(True)
        images = QWidget(self.window)
        layout = QVBoxLayout(images)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        for i, image in enumerate(self.imagesenu):
            w, h = image.size
            image_bytes = image.tobytes("raw", "RGB")

            qimg = QImage(image_bytes, w, h, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg).scaledToWidth(150, Qt.SmoothTransformation)
            
            
            image_label = QLabel(images)
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)

        scroll_area.setWidget(images)
        
        #self.thumbnail_viewer_result = self.thumbnail_viewer()
        self.stack_extract_widget.addWidget(scroll_area)
        self.window.Tabwidegts.removeTab(idx)
        self.window.Tabwidegts.insertTab(idx, self.stack_extract_widget, "Extract Pages")
        self.window.Tabwidegts.setCurrentIndex(idx)
        #self.stack_extract_widget.setCurrentIndex(0)
        self.stack_extract_widget.setCurrentIndex(1)
    """
    """
    def thumbnail_viewer(self):
        file_disposed = self.window.Tabwidegts.currentWidget()
        file_path_disposed = getattr(file_disposed, 'file_path', None)
        #print(f"Disposed file path: {file_path_disposed}")
        
        with open(file_path_disposed, "rb") as f_path_disposed:
            self.pdf_document_disposed = f_path_disposed.read()
        self.imagesenu = convert_from_bytes(self.pdf_document_disposed)
        scroll_area = QScrollArea(self.window)
        scroll_area.setWidgetResizable(True)
        images = QWidget(self.window)
        layout = QVBoxLayout(images)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        for i, image in enumerate(self.imagesenu):
            w, h = image.size
            image_bytes = image.tobytes("raw", "RGB")

            qimg = QImage(image_bytes, w, h, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg).scaledToWidth(150, Qt.SmoothTransformation)
            
            
            image_label = QLabel(images)
            image_label.setPixmap(pixmap)
            layout.addWidget(image_label)

        scroll_area.setWidget(images)
            #pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            #image_data = pix.tobytes("ppm")
            # Here you can create a QLabel or any widget to display the image
            # For example:
            #img_bytes = pix.tobytes("ppm")
            #image = QImage(img_bytes, pix.width, pix.height, pix.stride, QImage.Format_RGB8888)
            #image_label = QLabel(images)
           #image_label.setPixmap(QPixmap.fromImage(image))
           # layout.addWidget(image_label)

        return scroll_area

            # Add image_label to your layout

    """



    




        

        
        

        
        



    
