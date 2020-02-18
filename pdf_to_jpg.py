from PIL import Image
from pdf2image import convert_from_path
import sys
import os
import cv2 

def pdf_to_jpg(pdf):
    pages = convert_from_path(pdf, 500)
    basewidth = 600

    dir = os.path.join("jpg")
    if not os.path.exists(dir):
        os.mkdir(dir)

    for i, page in enumerate(pages):
        page.save("jpg/out_{}.jpg".format(i), "JPEG")

def resize_image(img, output):
    #percent by which the image is resized
    scale_percent = 15

    #calculate the 50 percent of original dimensions
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)

    # resize image
    output = cv2.resize(img, dsize)

    return output    