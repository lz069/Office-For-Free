# @Author: Zhi Li
# @Date: 2025-11-22 15:38:00
# @Project: free office tools

#%%
#import os,sys
import webbrowser
from pypdf import PdfReader as pr 
from pypdf import PdfWriter as pw
from pdf2image import convert_from_bytes, convert_from_path
import matplotlib.pyplot as plt
import pymupdf as fitz
import numpy as np
from timeit import default_timer as timer



file_path = r"C:/Users/MSI/Desktop/pdf-wangtest.pdf"
print(f"File path: {file_path}")

with open(file_path, "rb") as pdf_file:
    pdf_bytes = pdf_file.read()
    pdf_file.seek(0)
    pdf_reader = pr(pdf_file)
    





    pdf_pages = len(pdf_reader.pages)
    content_page1 = pdf_reader.pages
    #webbrowser.open(file_path)
    start1 = timer()
    page1_image = convert_from_bytes(pdf_bytes, 800)
    end1 = timer()
    print(f"Time taken to convert from bytes: {end1 - start1} seconds")
    #page1_image = convert_from_path(file_path, 300)
    start2 = timer()
    for i in range(len(page1_image)):
            plt.figure(figsize=(5, 6))
            plt.imshow(page1_image[i])
            plt.axis('off')
            plt.show()
        
    end2 = timer()
    print(f"Time taken to convert from path: {end2 - start2} seconds")
"""
pdffile = fitz.open('C:/Users/MSI/Desktop/pdf-wangtest.pdf')
page1 = pdffile.load_page(0)
page1_images = page1.get_pixmap(dpi=800)
pix = np.frombuffer(page1_images.samples, dtype=np.uint8).reshape(page1_images.height, page1_images.width, page1_images.n)
#page1_image = page1_images.tobytes()
plt.figure(figsize=(10, 12))
plt.imshow(pix)
plt.axis('off')
plt.show()

    #print(pdf_pages)
    #print(f"Content of page 1:\n{content_page1}")
    #print(f"Number of pages: {pdf_pages}")

"""





# %%
