from PIL import Image
from pdf2image import convert_from_path
import sys

def pdf_to_jpg(pdf):
    pages = convert_from_path(pdf, 500)

    for i, page in enumerate(pages):
        page.save('out_{}.jpg'.format(i), 'JPEG')
        