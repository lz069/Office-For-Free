
from pypdf import PdfReader, PdfWriter
import os, sys
from pdf2image import convert_from_path, convert_from_bytes
from PySide6.QtWidgets import QMainWindow, QApplication, QProgressBar, QFileDialog
from PySide6.QtCore import QTimer, Qt, QUrl, Slot
import fitz




#def pdf_splitter(pdf_path, output_path):
"""
Split a PDF file into individual pages and save them as separate PDF files.
"""

class ConvertImages:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.reader = PdfReader(pdf_path)

    def convert_pages_to_images(self, dpi=300):
        
        images = convert_from_path(self.pdf_path, dpi=dpi)
        return images

    


