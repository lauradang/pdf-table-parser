from pdf_to_jpg import pdf_to_jpg, resize_image
from crop import crop
from move_img import move_images
from format_df import create_dataframe
from editor import Editor
import os
import sys
import shutil
import cv2

# Convert pdfs to jpgs for OpenCV and OCR processing
pdf_to_jpg(sys.argv[1])
files = [file for file in os.listdir("jpg") if ".jpg" in file]

# Create visualize directory for Tkinter
dir = os.path.join("visualize")
if not os.path.exists(dir):
    os.mkdir(dir)
    
for file in files:
    img = crop(f"jpg/{file}", False) # Crop all jpgs into rectangles
    cv2.imwrite(f"visualize/{file}", resize_image(img, file))

for file in [file for file in os.listdir("visualize") if ".jpg" in file]:
    while True:
        print(f"Currently editing: {file}")
        app = Editor(f"visualize/{file}")
        app.mainloop()

dataframes = []

for file in files:
    move_images() # Move images into respective folders
    dataframes.append(create_dataframe()) # Create final pandas dataframe

    # Remove folders for next iteration
    shutil.rmtree("cropped_images")
    for dir in [dir for dir in os.listdir() if "output_" in dir]:
        shutil.rmtree(dir)

print(dataframes)


