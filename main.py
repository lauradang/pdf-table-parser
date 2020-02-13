from pdf_to_jpg import pdf_to_jpg
from crop import crop
from move_img import move_images
from format_df import create_dataframe
from gui import ImageFrame
import os
import sys
import shutil

# Convert pdfs to jpgs for OpenCV and OCR processing
pdf_to_jpg(sys.argv[1])

# Get all jpgs that were just converted
files = [file for file in os.listdir("jpg") if ".jpg" in file]

dataframes = []

for file in files:
    crop(f"jpg/{file}", True) # Crop all jpgs into rectangles

    move_images() # Move images into respective folders
    dataframes.append(create_dataframe()) # Create final pandas dataframe

    # Remove folders for next iteration
    shutil.rmtree("cropped_images")
    for dir in [dir for dir in os.listdir() if "output_" in dir]:
        shutil.rmtree(dir)

print(dataframes)


