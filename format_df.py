from PIL import Image
import pytesseract
import os
import pandas as pd
import re

def get_dirs():
    return [dir for dir in os.listdir() if "output_" in dir]

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def create_dataframe():
    data = []
    dirs = get_dirs()
    df = pd.DataFrame()

    for i, dir in enumerate(dirs):
        files = sorted_alphanumeric(os.listdir(dir))
        for file in files:
            text = pytesseract.image_to_string(Image.open(dir + "/" + file))
            data.append(text)
        df.insert(0, len(dirs)-1-i, data)
        data = []

    return df
