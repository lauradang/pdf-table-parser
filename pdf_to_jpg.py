from PIL import Image
from pdf2image import convert_from_path
import sys
import os

def pdf_to_jpg(pdf):
    pages = convert_from_path(pdf, 500)

    dir = os.path.join("jpg")
    if not os.path.exists(dir):
        os.mkdir(dir)

    for i, page in enumerate(pages):
        page.save('jpg/out_{}.jpg'.format(i), 'JPEG')
        