import os
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class pdfviewer(QWebEngineView):
    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path
        viewer = os.path.abspath(r"pdfjs-5.4.394-dist/web/viewer.html")

        url = QUrl.fromLocalFile(viewer)
        url.setQuery(f"file={QUrl.fromLocalFile(self.pdf_path).toString()}")
        self.load(url)